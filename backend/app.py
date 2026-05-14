from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz
import google.generativeai as genai
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash-8b")

skills_db = [
    "python","java","sql","machine learning","html","css",
    "javascript","react","node js","mongodb","aws","docker",
    "git","flask","django","tensorflow","deep learning",
    "full stack","api","mysql"
]

def extract_text(pdf_file):

    text = ""

    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text.lower()

def calculate_similarity(resume_text, job_desc):

    docs = [resume_text, job_desc]

    tfidf = TfidfVectorizer(stop_words='english')

    matrix = tfidf.fit_transform(docs)

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )

    return round(similarity[0][0] * 100, 2)

def skill_match(resume_text, job_desc):

    matched = []
    missing = []

    for skill in skills_db:

        if skill in job_desc.lower():

            if skill in resume_text:
                matched.append(skill)

            else:
                missing.append(skill)

    total = len(matched) + len(missing)

    score = 0 if total == 0 else (
        len(matched) / total
    ) * 100

    return matched, missing, round(score, 2)

def section_checker(resume_text):

    sections = [
        "skills",
        "projects",
        "education",
        "experience",
        "certification"
    ]

    missing = []

    for section in sections:

        if section not in resume_text:
            missing.append(section)

    return missing

def get_ai_feedback(resume_text, job_desc):

    try:

        prompt = f'''
        Analyze this resume.

        Resume:
        {resume_text[:3000]}

        Job:
        {job_desc}

        Give:
        1. strengths
        2. missing skills
        3. grammar improvements
        4. ATS suggestions
        5. final recommendation
        '''

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"AI feedback unavailable: {str(e)}"

def get_interview_questions(resume_text):

    try:

        prompt = f'''
        Generate 5 technical interview questions
        from this resume.

        Resume:
        {resume_text[:2000]}
        '''

        response = model.generate_content(prompt)

        return response.text

    except:

        return "Interview questions unavailable."

@app.route('/analyze', methods=['POST'])

def analyze_resume():

    try:

        pdf = request.files['resume']

        job_desc = request.form['jd']

        resume_text = extract_text(pdf)

        similarity_score = calculate_similarity(
            resume_text,
            job_desc
        )

        matched_skills, missing_skills, skill_score = skill_match(
            resume_text,
            job_desc
        )

        missing_sections = section_checker(
            resume_text
        )

        final_score = round(
            (similarity_score * 0.6) +
            (skill_score * 0.4),
            2
        )

        if final_score >= 80:
            rank = "Excellent Resume"

        elif final_score >= 60:
            rank = "Good Resume"

        else:
            rank = "Needs Improvement"

        improvement = round(
            100 - final_score,
            2
        )

        ai_feedback = get_ai_feedback(
            resume_text,
            job_desc
        )

        interview_questions = get_interview_questions(
            resume_text
        )

        return jsonify({

            "ats_score": final_score,

            "similarity_score": similarity_score,

            "skill_score": skill_score,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "missing_sections": missing_sections,

            "rank": rank,

            "improvement": improvement,

            "ai_feedback": ai_feedback,

            "interview_questions": interview_questions
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

if __name__ == '__main__':

    app.run(debug=True)