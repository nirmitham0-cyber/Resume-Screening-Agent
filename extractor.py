import re

# Common technical skills
COMMON_SKILLS = [
    "python", "java", "c", "c++", "sql", "mysql", 
    "html", "css", "javascript", "react", "node.js", "flask",
    "django", "git", "github", "docker", "aws", "azure",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn",
    "numpy", "pandas", "power bi", "excel"
]

# Education keywords mapped to a level, ordered highest priority first
# so the strongest qualification found is reported.
# Level: 2 = Bachelor's, 3 = Master's, 4 = PhD
EDUCATION_LEVELS = {
    "m.tech": 3,
    "mtech": 3,
    "m.sc": 3,
    "msc": 3,
    "mca": 3,
    "mba": 3,
    "master": 3,
    "b.tech": 2,
    "btech": 2,
    "b.sc": 2,
    "bsc": 2,
    "bca": 2,
    "b.e": 2,
    "be": 2,
    "bachelor": 2,
    "degree": 2,
}

# Check longer/more specific keywords first so "b.tech" is found
# before the generic "degree", and use word boundaries so short
# tokens like "be" don't match inside unrelated words (e.g. "before").
_EDUCATION_KEYWORDS_SORTED = sorted(
    EDUCATION_LEVELS.keys(), key=len, reverse=True
)


def _find_education(text):
    """
    Find the highest education qualification mentioned in the text.

    Returns:
        (label, level) e.g. ("b.tech", 2), or ("Not Specified", 0)
    """
    best_label = "Not Specified"
    best_level = 0

    for keyword in _EDUCATION_KEYWORDS_SORTED:
        escaped = re.escape(keyword)
        pattern = r'(?<![a-zA-Z])' + escaped + r'(?![a-zA-Z])'
        if re.search(pattern, text, flags=re.IGNORECASE):
            level = EDUCATION_LEVELS[keyword]
            if level > best_level:
                best_level = level
                best_label = keyword.upper()

    return best_label, best_level


def extract_resume_info(resume_text):
    """
    Extract Skills, Education and Experience
    from resume text.

    Returns:
    {
        "skills": [...],
        "education": "...",
        "education_level": int,
        "experience": ...
    }
    """

    text = resume_text.lower()

    # -------------------------
    # Extract Skills
    # -------------------------
    skills = []

    for skill in COMMON_SKILLS:
        if skill in text:
            skills.append(skill)

    skills = sorted(list(set(skills)))

    # -------------------------
    # Extract Education
    # -------------------------
    education, education_level = _find_education(text)

    # -------------------------
    # Extract Experience
    # -------------------------
    experience = "Fresher"

    patterns = [
        r'(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?'
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            experience = f"{match.group(1)} Years"
            break

    return {
        "skills": skills,
        "education": education,
        "education_level": education_level,
        "experience": experience
    }
