from parser import extract_text

resume_path = "resumes/Nirmitha_M.pdf"   # Change this to your resume file

text = extract_text(resume_path)

print(text)