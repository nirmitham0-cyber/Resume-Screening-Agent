from similarity import calculate_similarity


def calculate_final_score(jd_info, resume_info, jd_text, resume_text):
    """
    Calculate the final candidate score.

    Returns:
        final_score (0-100)
        details (dictionary)
    """

    # -------------------------------
    # 1. Semantic Similarity (50%)
    # -------------------------------
    semantic_score = calculate_similarity(jd_text, resume_text)

    # -------------------------------
    # 2. Skill Match (30%)
    # -------------------------------
    jd_skills = set(skill.lower() for skill in jd_info["skills"])
    resume_skills = set(skill.lower() for skill in resume_info["skills"])

    if len(jd_skills) == 0:
        skill_score = 100
    else:
        matched_skills = jd_skills.intersection(resume_skills)
        skill_score = (len(matched_skills) / len(jd_skills)) * 100

    # -------------------------------
    # 3. Education Match (10%)
    # Compares education LEVEL (Bachelor/Master/PhD), not exact wording,
    # so "B.Tech" correctly satisfies a "Bachelor's" requirement.
    # -------------------------------
    jd_edu_level = jd_info.get("education_level", 0)
    resume_edu_level = resume_info.get("education_level", 0)

    if jd_edu_level == 0:
        # JD did not specify an education requirement
        education_score = 100
    elif resume_edu_level >= jd_edu_level:
        education_score = 100
    elif resume_edu_level == 0:
        education_score = 0
    else:
        education_score = (resume_edu_level / jd_edu_level) * 100

    # -------------------------------
    # 4. Experience Match (10%)
    # -------------------------------
    if jd_info["experience"] is None:
        experience_score = 100

    elif resume_info["experience"].lower() == "fresher":
        experience_score = 0

    else:
        try:
            resume_years = int(resume_info["experience"].split()[0])

            if resume_years >= jd_info["experience"]:
                experience_score = 100
            else:
                experience_score = (
                    resume_years / jd_info["experience"]
                ) * 100

        except Exception:
            experience_score = 0

    # -------------------------------
    # Final Weighted Score
    # -------------------------------
    final_score = (
        semantic_score * 0.50 +
        skill_score * 0.30 +
        education_score * 0.10 +
        experience_score * 0.10
    )

    final_score = round(final_score, 2)

    return final_score, {
        "semantic_score": round(semantic_score, 2),
        "skill_score": round(skill_score, 2),
        "education_score": round(education_score, 2),
        "experience_score": round(experience_score, 2),
        "matched_skills": list(jd_skills.intersection(resume_skills)),
        "missing_skills": list(jd_skills - resume_skills)
    }
