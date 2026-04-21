def generate_explanation(result: dict, candidate_name: str) -> str:
    score = result["final_score"]
    matched = result["matched_skills"]
    missing = result["missing_skills"]

    strengths = []
    if result["skill_score"] >= 70:
        strengths.append("strong skill alignment with the job description")
    if result["experience_score"] >= 70:
        strengths.append("relevant experience level")
    if result["education_score"] >= 70:
        strengths.append("suitable educational background")
    if result["semantic_score"] >= 70:
        strengths.append("high overall semantic similarity to the job requirements")

    if not strengths:
        strengths.append("some alignment with the position requirements")

    explanation = (
        f"{candidate_name} received a score of {score}%. "
        f"The candidate shows {', '.join(strengths)}."
    )

    if matched:
        explanation += f" Matched skills include: {', '.join(matched[:8])}."
    if missing:
        explanation += f" Missing or less visible skills include: {', '.join(missing[:8])}."

    return explanation