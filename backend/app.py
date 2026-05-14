from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

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
    "deep learning",
    "full stack"
]

# Extract text from PDF
def extract_text(pdf_file):

    text = ""

    pdf = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    for page in pdf:
        text += page.get_text()

    return text.lower()


# Similarity Score
def calculate_similarity(
    resume_text,
    job_desc
):

    documents = [
        resume_text,
        job_desc
    ]

    tfidf = TfidfVectorizer(
        stop_words='english'
    )

    tfidf_matrix = tfidf.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    return round(
        similarity[0][0] * 100,
        2
    )


# Skill Matching
def skill_match(
    resume_text,
    job_desc
):

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
        score = (
            len(matched) /
            total_skills
        ) * 100

    return matched, missing, round(score, 2)


# Resume Sections
def section_checker(
    resume_text
):

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


# Rank Resume
def resume_rank(score):

    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    else:
        return "Needs Improvement"


# API Route
@app.route('/analyze', methods=['POST'])
def analyze_resume():

    try:

        # Get Data
        pdf = request.files['resume']
        job_desc = request.form['job_desc']

        # Extract Resume Text
        resume_text = extract_text(pdf)

        # Similarity
        similarity_score = calculate_similarity(
            resume_text,
            job_desc
        )

        # Skills
        matched_skills, missing_skills, skill_score = skill_match(
            resume_text,
            job_desc
        )

        # Missing Sections
        missing_sections = section_checker(
            resume_text
        )

        # Final ATS Score
        final_score = round(
            (similarity_score * 0.6) +
            (skill_score * 0.4),
            2
        )

        # Improvement
        improvement_needed = round(
            100 - final_score,
            2
        )

        # Rank
        rank = resume_rank(
            final_score
        )

        # Static AI Feedback
        ai_feedback = """
• Improve resume formatting
• Add more technical projects
• Include certifications
• Add measurable achievements
"""

        # Static Interview Questions
        interview_questions = [
            "Tell me about yourself",
            "Explain your projects",
            "What are your strengths?",
            "Why should we hire you?",
            "Explain your technical skills"
        ]

        # JSON Response
        return jsonify({

            "ats_score": final_score,

            "similarity_score": similarity_score,

            "skill_score": skill_score,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "missing_sections": missing_sections,

            "rank": rank,

            "improvement_needed": improvement_needed,

            "ai_feedback": ai_feedback,

            "interview_questions": interview_questions
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# Run App
if __name__ == '__main__':

    app.run(debug=True)