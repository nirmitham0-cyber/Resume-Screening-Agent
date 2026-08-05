from parser import extract_text
from extractor import extract_resume_info

# Change filename if needed
resume_text = extract_text("resumes/Nirmitha_M.pdf")

result = extract_resume_info(resume_text)

print("\nExtracted Resume Information\n")
print(result)