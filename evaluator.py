import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
def extract_json(text):
    text = re.sub(r"```json|```", "", text)

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return match.group(0)

    return text.strip()
def is_valid_resume(text):
    if not text or len(text.strip()) < 50:
        return False, "Resume is too short or empty"

    text_lower = text.lower()

    # basic resume indicators
    keywords = [
        "experience", "project", "skills",
        "education", "worked", "developed"
    ]

    matches = sum(k in text_lower for k in keywords)

    if matches < 2:
        return False, "Content does not look like a valid resume"

    return True, ""

# -------- CLEAN JSON -------- #
def clean_json(text):
    text = re.sub(r"```json|```", "", text)
    return text.strip()

# -------- LLM CALL -------- #
def call_llm(prompt):
    response = model.generate_content(prompt)
    return response.text


# -------- EVALUATE -------- #
def evaluate_resume(resume, jd):
    valid, message = is_valid_resume(resume)

    if not valid:
     return {
        "name": "invalid",
        "final_score": 0,
        "verdict": "Reject",
        "reason": message,
        "validation": {
            "credibility_score": 0,
            "severity": "High",
            "confidence": "Low",
            "red_flags": ["Invalid or empty resume"],
            "explanation": message
        }
    }
    
    
    
    
    
    prompt = f"""
You are an expert AI Resume Evaluator acting like a senior recruiter.

IMPORTANT:
- Go beyond keyword matching
- Consider transferable skills
- Return ONLY valid JSON


Resume:
{resume}

Job Description:
{jd}
Evaluate the candidate on these 4 dimensions:

1. Skill Match (required vs actual skills)
2. Depth of Experience (projects, usage, years, complexity)
3. Role Alignment (how well profile fits the job role)
4. Additional Strengths (projects, extracurriculars, achievements)
Return JSON:

{{
  "name": "candidate",
  "skill_score": number,
  "experience_score": number,
  "project_score": number,
  "strengths": [],
  "gaps": [],
  "transferable_skills": [],
  "verdict": "",
  "reason": ""
}}
"""

    # -------- FIRST PASS -------- #
    raw = call_llm(prompt)
    raw = clean_json(raw)

    # extract valid JSON block (Gemini safety)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        raw = match.group(0)

    try:
        data = json.loads(raw)
    except:
        data = {
            "name": "unknown",
            "skill_score": 0,
            "experience_score": 0,
            "project_score": 0,
            "strengths": [],
            "gaps": ["Parsing failed"],
            "transferable_skills": [],
            "verdict": "Unknown",
            "reason": "Parsing failed"
        }
    
    # -------- NORMALIZE SCORES -------- #

    def normalize_score(value):
      if value <= 10:
          return value * 10
      return value

    data["skill_match"] = normalize_score(data.get("skill_match", 0))
    data["depth_of_experience"] = normalize_score(data.get("depth_of_experience", 0))
    data["role_alignment"] = normalize_score(data.get("role_alignment", 0))
    data["additional_strengths"] = normalize_score(data.get("additional_strengths", 0))
    # -------- BASE SCORE -------- #
    base_score = (
    data.get("skill_match", 0) * 0.35 +
    data.get("depth_of_experience", 0) * 0.30 +
    data.get("role_alignment", 0) * 0.25 +
    data.get("additional_strengths", 0) * 0.10
)

    # -------- SECOND PASS (VALIDATION) -------- #
    validation = validate_candidate(data, jd)

    # attach validation output
    data["validation"] = validation

    cred_score = validation.get("credibility_score", 50)
    print(base_score)
    # -------- FINAL SCORE -------- #
    final_score = 0.7 * base_score + 0.2 * cred_score

    # penalty based on severity
    severity = validation.get("severity", "Low")

    if severity == "High":
        final_score *= 0.85
    elif severity == "Medium":
        final_score *= 0.92
    print(final_score)
    data["final_score"] = round(final_score, 2)

    return data


# -------- RANK -------- #
def rank_candidates(candidates):
    ranked = sorted(
        candidates,
        key=lambda x: x.get("final_score", 0),
        reverse=True
    )

    output = []

    for i, c in enumerate(ranked):
        output.append({
            "rank": i + 1,
            "name": c.get("name", f"Candidate {i+1}"),
            "score": c.get("final_score", 0),
            "verdict": c.get("verdict", ""),
            "credibility": c.get("validation", {}).get("confidence", ""),
            "red_flags": c.get("validation", {}).get("red_flags", []),
            "reason": c.get("reason", "")
        })

    return output
def validate_candidate(candidate, jd):
    prompt = f"""
You are a senior recruiter performing a SECOND PASS validation.

Your job is to critically evaluate the candidate's credibility.

Check for:

1. Misleading or exaggerated claims
2. Irrelevant information for the role
3. Lack of measurable results or impact
4. Repetitive or suspicious content

IMPORTANT:
- Be strict and skeptical
- Do NOT trust the resume blindly
- Look for evidence vs claims
Be realistic for the candidate’s experience level.
Do NOT penalize students for lacking industry experience.
Do NOT treat missing preferred skills as major red flags.

Candidate Data:
{candidate}

Job Description:
{jd}

Return STRICT JSON:

{{
  "credibility_score": number (0-100),
  "red_flags": [],
  "severity": "Low/Medium/High",
  "confidence": "High/Medium/Low",
  "explanation": ""
}}
"""

    raw = call_llm(prompt)
    raw = extract_json(raw)

    try:
      return json.loads(raw)
    except:
        return {
            "credibility_score": 50,
            "red_flags": ["Validation failed"],
            "severity": "Medium",
            "confidence": "Low",
            "explanation": "Validation parsing failed"
        }