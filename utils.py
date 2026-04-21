import re


SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "c++", "sql", "html", "css",
    "react", "next.js", "node.js", "flask", "django", "fastapi", "streamlit",
    "machine learning", "deep learning", "nlp", "tensorflow", "pytorch",
    "data analysis", "pandas", "numpy", "scikit-learn", "git", "docker",
    "aws", "azure", "mongodb", "postgresql", "mysql", "power bi", "excel"
]

EDUCATION_KEYWORDS = [
    "bachelor", "master", "phd", "computer science", "software engineering",
    "information technology", "artificial intelligence", "data science"
]


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_skills(text: str):
    cleaned = clean_text(text)
    found = [skill for skill in SKILL_KEYWORDS if skill in cleaned]
    return sorted(list(set(found)))


def extract_education_score(text: str) -> float:
    cleaned = clean_text(text)
    score = 0.0

    if "phd" in cleaned:
        score = 1.0
    elif "master" in cleaned:
        score = 0.85
    elif "bachelor" in cleaned:
        score = 0.7

    if any(field in cleaned for field in EDUCATION_KEYWORDS):
        score = max(score, 0.75)

    return score


def extract_experience_score(text: str, jd_text: str) -> float:
    cleaned_resume = clean_text(text)
    cleaned_jd = clean_text(jd_text)

    years_patterns = re.findall(r'(\d+)\+?\s+years?', cleaned_resume)
    years = max([int(y) for y in years_patterns], default=0)

    required_patterns = re.findall(r'(\d+)\+?\s+years?', cleaned_jd)
    required_years = max([int(y) for y in required_patterns], default=2)

    if years >= required_years:
        return 1.0
    elif years == required_years - 1:
        return 0.75
    elif years > 0:
        return 0.5
    return 0.2