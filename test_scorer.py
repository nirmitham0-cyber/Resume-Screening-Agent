from parser import extract_text
from extractor import extract_resume_info
from jd_parser import parse_job_description
from scorer import calculate_final_score

# Read JD
with open("jd.txt", "r", encoding="utf-8") as file:
    jd_text = file.read()

# Read Resume
resume_text = extract_text("resumes/Nirmitha_M.pdf")

# Extract information
jd_info = parse_job_description(jd_text)
resume_info = extract_resume_info(resume_text)

# Calculate score
score, details = calculate_final_score(
    jd_info,
    resume_info,
    jd_text,
    resume_text
)

print("\nCandidate Score")
print("-------------------------")
print("Final Score:", score)

print("\nDetails")
for key, value in details.items():
    print(f"{key}: {value}")