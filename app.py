from flask import Flask, request, jsonify
from flask import render_template
from evaluator import evaluate_resume, rank_candidates
from utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


# -------- SINGLE EVAL -------- #
@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.json
    resume = data.get("resume")
    jd = data.get("jd")

    result = evaluate_resume(resume, jd)
    return jsonify(result)


# -------- MULTI RANK -------- #
@app.route("/rank", methods=["POST"])
def rank():
    data = request.json
    resumes = data.get("resumes", [])
    jd = data.get("jd")

    results = []
    for r in resumes:
        results.append(evaluate_resume(r, jd))

    ranked = rank_candidates(results)
    return jsonify(ranked)
@app.route("/upload-evaluate", methods=["POST"])
def upload_evaluate():
    resume_file = request.files["resume"]
    jd_file = request.files.get("jd_file")
    jd_text = request.form.get("jd_text")

    # -------- RESUME -------- #
    resume_text = extract_text_from_pdf(resume_file)

    # -------- JD -------- #
    if jd_file:
        jd_filename = jd_file.filename.lower()

        if jd_filename.endswith(".pdf"):
            jd = extract_text_from_pdf(jd_file)
        elif jd_filename.endswith(".txt"):
            jd = jd_file.read().decode("utf-8")
        else:
            return jsonify({"error": "Unsupported JD format"}), 400
    else:
        jd = jd_text  # fallback

    result = evaluate_resume(resume_text, jd)
    return jsonify(result)
@app.route("/upload-rank", methods=["POST"])
def upload_rank():
    files = request.files.getlist("resumes")
    jd_file = request.files.get("jd_file")
    jd_text = request.form.get("jd_text")

    # JD handling
    if jd_file:
        jd = extract_text_from_pdf(jd_file)
    else:
        jd = jd_text

    candidates = []

    for file in files:
        resume_text = extract_text_from_pdf(file)
        result = evaluate_resume(resume_text, jd)
        candidates.append(result)

    ranked = rank_candidates(candidates)
    return jsonify(ranked)
if __name__ == "__main__":
    app.run(debug=True)