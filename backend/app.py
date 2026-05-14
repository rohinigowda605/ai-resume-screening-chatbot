@app.route('/analyze', methods=['POST'])
def analyze_resume():

    try:

        # Safe request handling
        pdf = request.files.get('resume')
        job_desc = request.form.get('job_desc')

        if not pdf:
            return jsonify({
                "error": "Resume file missing"
            }), 400

        if not job_desc:
            return jsonify({
                "error": "Job description missing"
            }), 400

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

        # Rank
        if final_score >= 80:
            rank = "Excellent"
        elif final_score >= 60:
            rank = "Good"
        else:
            rank = "Needs Improvement"

        # Improvement %
        improvement_needed = round(100 - final_score, 2)

        # AI Feedback
        ai_feedback = "AI feedback unavailable."

        try:
            from gemini_helper import get_ai_feedback

            ai_feedback = get_ai_feedback(
                resume_text,
                job_desc,
                missing_skills
            )

        except Exception as ai_error:
            ai_feedback = f"AI feedback unavailable: {str(ai_error)}"

        # Interview Questions
        interview_questions = []

        try:
            interview_questions = [
                f"Explain your experience with {skill}"
                for skill in matched_skills[:5]
            ]

        except:
            interview_questions = []

        # Final Response
        return jsonify({

            "ats_score": final_score,

            "similarity_score": similarity_score,

            "skill_score": skill_score,

            "rank": rank,

            "improvement_needed": improvement_needed,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "missing_sections": missing_sections,

            "ai_feedback": ai_feedback,

            "interview_questions": interview_questions
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500