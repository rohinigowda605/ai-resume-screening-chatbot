from flask import Flask, request, jsonify
from flask_cors import CORS
from parser import extract_text
from skills import extract_skills
from matcher import match_resume, missing_skills, calculate_scores
from ai_helper import get_ai_feedback

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        print("REQUEST RECEIVED")   # Debug print

        if "resume" not in request.files:
            return jsonify({"error": "No resume uploaded"}), 400

        resume_file = request.files["resume"]
        jd_text = request.form.get("jd", "")

        # Extract text
        resume_text = extract_text(resume_file)

        # Extract skills
        resume_sk = extract_skills(resume_text)
        jd_sk = extract_skills(jd_text)

        # Matching
        similarity = match_resume(resume_text, jd_text)
        scores = calculate_scores(resume_sk, jd_sk, similarity)

        # Missing skills
        missing = missing_skills(resume_sk, jd_sk)

        # TEMP AI (no API)
        ai_feedback =  get_ai_feedback(resume_text, jd_text, missing)

        return jsonify({
            "scores": scores,
            "missing_skills": missing,
            "ai_feedback": ai_feedback
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🚀 Server starting...")
    app.run(debug=True)
    
    import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))