import streamlit as st
from sentence_transformers import SentenceTransformer, util
from utils import extract_skills, extract_education_score, extract_experience_score


@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


def semantic_similarity(resume_text: str, jd_text: str) -> float:
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(jd_text, convert_to_tensor=True)
    score = util.cos_sim(emb1, emb2).item()
    return max(0.0, min((score + 1) / 2, 1.0))


def skill_match_score(resume_text: str, jd_text: str):
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    if not jd_skills:
        return 0.5, list(resume_skills), []

    matched = list(resume_skills.intersection(jd_skills))
    missing = list(jd_skills - resume_skills)
    score = len(matched) / len(jd_skills) if jd_skills else 0.0

    return score, matched, missing


def calculate_final_score(resume_text: str, jd_text: str):
    skill_score, matched_skills, missing_skills = skill_match_score(resume_text, jd_text)
    experience_score = extract_experience_score(resume_text, jd_text)
    education_score = extract_education_score(resume_text)
    semantic_score = semantic_similarity(resume_text, jd_text)

    final_score = (
        skill_score * 0.40 +
        experience_score * 0.25 +
        education_score * 0.15 +
        semantic_score * 0.20
    ) * 100

    return {
        "final_score": round(final_score, 2),
        "skill_score": round(skill_score * 100, 2),
        "experience_score": round(experience_score * 100, 2),
        "education_score": round(education_score * 100, 2),
        "semantic_score": round(semantic_score * 100, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }