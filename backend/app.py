from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz
import os
import google.generativeai as genai

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Gemini API Setup
genai.configure(api_key=os.getenv("AIzaSyAHoJtYe9GHCro5kDWzlczg3ULgYLNN8bU"))

model = genai.GenerativeModel("gemini-1.5-flash")

# Skills Database
skills_db = [
    "python",
    "java",
    "sql",
    "machine learning",
    "html",
    "css",
    "javascript",
    "react",
    "node js",
    "mongodb",
    "aws",
    "docker",
    "git",
    "flask",
    "django",
    "tensorflow",
    "deep learning"
]

# Extract text from PDF
def extract_text(pdf_file):

    text = ""

    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text.lower()


# ATS Similarity Score
def calculate_similarity(resume_text, job_desc):

    documents = [resume_text, job_desc]

    tfidf = TfidfVectorizer(stop_words='english')

    tfidf_matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    return round(similarity[0][0] * 100, 2)


# Skill Matching
def skill_match(resume_text, job_desc):

    matched = []
    missing = []

    for skill in skills_db:

        if skill in job_desc.lower():

            if skill in resume_text:
                matched.append(skill)

            else:
                missing.append(skill)

    total_skills = len(matched) + len(missing)

    if total_skills == 0:
        score = 0

    else:
        score = (len(matched) / total_skills) * 100

    return matched, missing, round(score, 2)


# Resume Section Checker
def section_checker(resume_text):

    sections = [
        "skills",
        "projects",
        "education",
        "experience",
        "certification"
    ]

    missing_sections = []

    for section in sections:

        if section not in resume_text:
            missing_sections.append(section)

    return missing_sections


# Gemini AI Feedback
def generate_ai_feedback(
    resume_text,
    job_desc,
    missing_skills,
    final_score
):

    prompt = f"""
    You are an AI career coach.

    ATS Score: {final_score}

    Missing Skills:
    {", ".join(missing_skills)}

    Resume:
    {resume_text[:1000]}

    Job Description:
    {job_desc[:1000]}

    Give:
    1. Resume improvement tips
    2. Missing technical skills
    3. ATS optimization suggestions
    4. Career advice

    Keep response short and professional.
    """

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        print("Gemini Error:", e)

        return "AI feedback not available right now."


# Main API
@app.route('/analyze', methods=['POST'])
def analyze_resume():

    try:

        # Get files/data
        pdf = request.files['resume']

        job_desc = request.form['job_desc']

        # Extract resume text
        resume_text = extract_text(pdf)

        # Similarity Score
        similarity_score = calculate_similarity(
            resume_text,
            job_desc
        )

        # Skill Match
        matched_skills, missing_skills, skill_score = skill_match(
            resume_text,
            job_desc
        )

        # Missing Sections
        missing_sections = section_checker(resume_text)

        # Final ATS Score
        final_score = round(
            (similarity_score * 0.6) +
            (skill_score * 0.4),
            2
        )

        # Gemini AI Feedback
        ai_feedback = generate_ai_feedback(
            resume_text,
            job_desc,
            missing_skills,
            final_score
        )

        # Suggestions
        suggestions = []

        if missing_skills:

            suggestions.append(
                "Add these skills: " +
                ", ".join(missing_skills)
            )

        if missing_sections:

            suggestions.append(
                "Add sections: " +
                ", ".join(missing_sections)
            )

        if final_score < 50:

            suggestions.append(
                "Resume needs major improvement for ATS systems."
            )

        elif final_score < 75:

            suggestions.append(
                "Resume is good but can be improved."
            )

        else:

            suggestions.append(
                "Resume is ATS optimized."
            )

        # JSON Response
        return jsonify({

            "ats_score": final_score,

            "similarity_score": similarity_score,

            "skill_score": skill_score,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "missing_sections": missing_sections,

            "suggestions": suggestions,

            "ai_feedback": ai_feedback
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# Run Server
if __name__ == '__main__':

    app.run(debug=True)