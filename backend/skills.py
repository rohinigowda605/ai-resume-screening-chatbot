
SKILL_DB = [
    "python", "java", "c++", "sql", "machine learning",
    "deep learning", "html", "css", "javascript",
    "react", "node", "flask", "django"
]

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILL_DB:
        if skill in text:
            found.append(skill)
    return list(set(found))