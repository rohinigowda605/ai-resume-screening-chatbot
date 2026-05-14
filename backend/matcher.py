from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Resume Similarity
def match_resume(resume, jd):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([
        resume,
        jd
    ])

    score = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]

    return round(score * 100, 2)


# ATS + Skill Scores
def calculate_scores(
    resume_skills,
    jd_skills,
    similarity_score
):

    matched = len(
        set(resume_skills) &
        set(jd_skills)
    )

    total = len(jd_skills)

    if total == 0:
        skill_match = 0

    else:
        skill_match = (
            matched / total
        ) * 100

    ats_score = (
        0.6 * similarity_score
    ) + (
        0.4 * skill_match
    )

    return {

        "similarity_score":
        round(similarity_score, 2),

        "skill_match":
        round(skill_match, 2),

        "ats_score":
        round(ats_score, 2)
    }


# Missing Skills
def missing_skills(
    resume_skills,
    jd_skills
):

    return list(
        set(jd_skills) -
        set(resume_skills)
    )


# Resume Ranking
def resume_rank(score):

    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    else:
        return "Needs Improvement"