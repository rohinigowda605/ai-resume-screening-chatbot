import os
from openai import OpenAI

client = OpenAI()

def get_ai_feedback(resume_text, jd_text, missing_skills):
    try:
        prompt = f"""
        You are an expert AI career coach.

        Resume:
        {resume_text[:500]}

        Job Description:
        {jd_text[:500]}

        Missing Skills:
        {missing_skills}

        Give:
        1. Specific resume improvements
        2. Skills to learn
        3. 1-2 project ideas

        Keep it short and clear.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", str(e))
        return "AI feedback not available right now."