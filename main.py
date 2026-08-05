import os

from parser import extract_text
from jd_parser import parse_job_description
from extractor import extract_resume_info
from scorer import calculate_final_score
from llm import analyze_resume
from exporter import export_results


# -----------------------------
# Configuration
# -----------------------------
RESUME_FOLDER = "resumes"
JOB_DESCRIPTION_FILE = "jd.txt"


# -----------------------------
# Read Job Description
# -----------------------------
with open(JOB_DESCRIPTION_FILE, "r", encoding="utf-8") as file:
    jd_text = file.read()

jd_info = parse_job_description(jd_text)


# -----------------------------
# Process Resumes
# -----------------------------
results = []

supported_extensions = [".pdf", ".docx", ".txt"]

for filename in os.listdir(RESUME_FOLDER):

    extension = os.path.splitext(filename)[1].lower()

    if extension not in supported_extensions:
        continue

    resume_path = os.path.join(RESUME_FOLDER, filename)

    print(f"\nProcessing: {filename}")

    try:

        # Read Resume
        resume_text = extract_text(resume_path)

        # Extract Information
        resume_info = extract_resume_info(resume_text)

        # Calculate Final Score
        final_score, details = calculate_final_score(
            jd_info,
            resume_info,
            jd_text,
            resume_text
        )

        # AI Explanation
        explanation = analyze_resume(
            jd_text,
            resume_text
        )

        results.append({

            "Candidate": filename,

            "Final Score": final_score,

            "Semantic Score": details["semantic_score"],

            "Skill Score": details["skill_score"],

            "Education Score": details["education_score"],

            "Experience Score": details["experience_score"],

            "Matched Skills": ", ".join(details["matched_skills"]),

            "Missing Skills": ", ".join(details["missing_skills"]),

            "LLM Analysis": explanation

        })

    except Exception as error:

        print(f"Error processing {filename}: {error}")


# -----------------------------
# Ranking
# -----------------------------
results.sort(
    key=lambda candidate: candidate["Final Score"],
    reverse=True
)

for index, candidate in enumerate(results, start=1):

    candidate["Rank"] = index


# -----------------------------
# Export Results
# -----------------------------
export_results(results)


# -----------------------------
# Print Ranking
# -----------------------------
print("\n")
print("=" * 60)
print("FINAL RANKING")
print("=" * 60)

for candidate in results:

    print(
        f"Rank {candidate['Rank']} | "
        f"{candidate['Candidate']} | "
        f"Score: {candidate['Final Score']}"
    )

print("\nProject Completed Successfully.")