import google.generativeai as genai
import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "models/gemini-1.5-flash"
)

def get_ai_feedback(
    resume_text,
    job_desc,
    missing_skills
):

    try:

        prompt = f"""
        Analyze this resume.

        Resume:
        {resume_text[:3000]}

        Job Description:
        {job_desc}

        Missing Skills:
        {", ".join(missing_skills)}

        Give ATS improvement suggestions.
        """

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return str(e)