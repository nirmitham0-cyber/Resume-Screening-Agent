from jd_parser import parse_job_description

with open("jd.txt", "r", encoding="utf-8") as file:
    jd_text = file.read()

result = parse_job_description(jd_text)

print("\nParsed Job Description\n")
print(result)