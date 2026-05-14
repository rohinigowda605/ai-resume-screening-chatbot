import google.generativeai as genai
import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-pro"
)

def get_ai_feedback(
    resume_text,
    job_desc,
    missing_skills
):

    try:

        prompt = f"""
        Analyze this resume for ATS.

        Resume:
        {resume_text[:3000]}

        Job Description:
        {job_desc}

        Missing Skills:
        {", ".join(missing_skills)}

        Give:
        1. ATS improvements
        2. Resume improvements
        3. Missing skills
        4. Career suggestions
        """

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"Gemini Error: {str(e)}"