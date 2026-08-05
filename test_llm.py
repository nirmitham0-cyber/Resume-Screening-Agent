from parser import extract_text
from llm import analyze_resume

# Read Job Description
with open("jd.txt", "r", encoding="utf-8") as file:
    jd = file.read()

# Read Resume
resume = extract_text("resumes/Nirmitha_M.pdf")

# Analyze
result = analyze_resume(jd, resume)

print(result)