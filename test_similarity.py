from parser import extract_text
from similarity import calculate_similarity

# Read Job Description
with open("jd.txt", "r", encoding="utf-8") as file:
    jd = file.read()

# Read Resume
resume = extract_text("resumes/Nirmitha_M.pdf")

# Calculate similarity
score = calculate_similarity(jd, resume)

print("\nSemantic Similarity Score")
print("-------------------------")
print(f"Score : {score}%")