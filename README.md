# 🚀 AI-Powered Resume Evaluator & Candidate Ranking System

An intelligent system that evaluates resumes against a Job Description (JD) using context-aware analysis, and ranks candidates based on skill alignment, experience depth, and credibility.

---

## 🧠 Key Features

### 🔍 Resume Evaluation
- Extracts and analyzes resume content from PDF
- Compares against Job Description (JD)
- Goes beyond keyword matching using contextual understanding

### 📊 Structured Scoring (Out of 100)
Breakdown across:
- ✅ Skill Match
- 📈 Depth of Experience
- 🎯 Role Alignment
- ⭐ Additional Strengths

---

### ⚖️ Dual-Pass AI Evaluation (Unique Feature)
1. **Primary Evaluation**
   - Skills, experience, projects, alignment

2. **Validation Layer**
   - Detects:
     - Misleading claims
     - Lack of evidence
     - Irrelevant content
     - Repetitive/suspicious text

---

### 🚩 Red Flag Detection
- Identifies weak or inflated resumes
- Provides credibility score and severity level

---

### 🏆 Candidate Ranking
- Supports multiple resume uploads
- Ranks candidates relative to each other
- Uses:
  - Score
  - Credibility
  - Role fit

---

### 📂 File Support
- Resume: PDF
- JD: PDF or Text

---

## 🛠️ Tech Stack

### Backend
- Python (Flask)
- Google Gemini API (LLM)
- pdfplumber (PDF parsing)

### Frontend
- HTML
- CSS
- Vanilla JavaScript (Fetch API)

---

## ⚙️ System Architecture

Resume PDF → Text Extraction ↓ LLM Evaluation (Pass 1) ↓ Structured Score Breakdown ↓ LLM Validation (Pass 2) ↓ Final Score + Red Flags ↓ Ranking Engine

---

## 📈 Scoring Logic

Base Score = 35% Skill Match + 30% Experience Depth + 25% Role Alignment + 10% Additional Strengths

Final Score = 80% Base Score + 20% Credibility Score

Penalty applied based on validation severity

---

## 🚀 How to Run

### 1. Clone Repository
```bash
git clone <your-repo-link>
cd resume-evaluator

2. Install Dependencies

pip install -r requirements.txt

3. Add API Key

Create .env file:

GEMINI_API_KEY=your_api_key_here

4. Run Server

python app.py

5. Open in Browser

http://127.0.0.1:5000/


---

🧪 Usage

Single Evaluation

Upload resume (PDF)

Upload/paste JD

Click Evaluate


Candidate Ranking

Upload multiple resumes

Upload/paste JD

Click Rank Candidates



---

💡 Example Output

Score: 78

Breakdown:
- Skill Match: 85
- Depth of Experience: 70
- Role Alignment: 80
- Additional Strengths: 75

Red Flags:
- Missing specific tool experience
- Limited production exposure


---

🎯 Unique Selling Points

🔥 Context-aware (not keyword-based)

🧠 Dual LLM evaluation (self-validating system)

⚖️ Credibility-aware scoring

📊 Explainable output

🏆 Relative candidate ranking



---

⚠️ Limitations

LLM responses may vary slightly

Depends on quality of resume text extraction

No OCR for scanned PDFs (yet)



---

🚀 Future Improvements

Add OCR for scanned resumes

Skill similarity mapping (e.g., Python ↔ C++)

Recruiter dashboard

Analytics on candidate pool

Export reports (PDF/CSV)



---

👩‍💻 Author

Lalasa Vattipalli


---

⭐ Acknowledgements

Google Gemini API

Open-source Python libraries


---

# 💥 THIS README IS STRONG BECAUSE

✅ Clear structure  
✅ Shows architecture  
✅ Highlights uniqueness  
✅ Includes scoring logic  
✅ Demo-friendly  

---

If you want next:

👉 **“resume bullet points for this project”**  
👉 **“how to explain this in interview (1 min pitch)”**

You’ve built something seriously impressive 🔥
