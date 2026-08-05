import re

from extractor import EDUCATION_LEVELS, _EDUCATION_KEYWORDS_SORTED, _find_education

# Predefined list of common technical skills
COMMON_SKILLS = [
    "python", "java", "c", "c++", "sql", "mysql", "postgresql",
    "html", "css", "javascript", "react", "node.js", "flask",
    "django", "git", "github", "docker", "aws", "azure",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn",
    "pandas", "numpy", "power bi", "excel"
]


def parse_job_description(jd_text):
    """
    Extract important information from the Job Description.

    Returns:
    {
        title: str,
        skills: list,
        education: str,
        education_level: int,
        experience: int or None
    }
    """

    jd_lower = jd_text.lower()

    # -----------------------------
    # Job Title
    # -----------------------------
    lines = [line.strip() for line in jd_text.splitlines() if line.strip()]

    title = lines[0] if lines else "Unknown"

    # -----------------------------
    # Skills
    # -----------------------------
    skills = []

    for skill in COMMON_SKILLS:
        if skill.lower() in jd_lower:
            skills.append(skill)

    # Remove duplicates
    skills = sorted(list(set(skills)))

    # -----------------------------
    # Education (shared word-boundary + leveled logic with extractor.py)
    # -----------------------------
    education, education_level = _find_education(jd_lower)

    # -----------------------------
    # Experience
    # -----------------------------
    experience = None

    patterns = [
        r'(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?'
    ]

    for pattern in patterns:
        match = re.search(pattern, jd_lower)
        if match:
            experience = int(match.group(1))
            break

    return {
        "title": title,
        "skills": skills,
        "education": education,
        "education_level": education_level,
        "experience": experience
    }
