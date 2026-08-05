# Scoring Method

The Resume Screening Agent evaluates each resume using a weighted scoring
approach that combines objective NLP similarity with structured data
matching, plus an LLM-generated explanation.

## 1. Text Extraction
Resume and Job Description text is extracted from PDF, DOCX, or TXT files
(`parser.py`).

## 2. Information Extraction
Skills, education level, and years of experience are extracted from both
the Job Description (`jd_parser.py`) and each resume (`extractor.py`) using
keyword and pattern matching. Education is normalized to a level
(Bachelor's = 2, Master's = 3, PhD = 4) rather than matched as exact text,
so a candidate's "B.Tech" correctly satisfies a "Bachelor's degree"
requirement.

## 3. Semantic Similarity
The Job Description and resume text are each converted into sentence
embeddings using the `all-MiniLM-L6-v2` Sentence Transformer model.
Cosine similarity between the two embeddings produces a 0-100 semantic
similarity score (`similarity.py`).

## 4. Weighted Final Score
```
Final Score = (0.50 × Semantic Similarity)
            + (0.30 × Skill Match %)
            + (0.10 × Education Match)
            + (0.10 × Experience Match)
```

- **Skill Match** = percentage of required JD skills found in the resume.
- **Education Match** = 100 if the candidate's education level meets or
  exceeds the JD's required level (or if the JD specifies no requirement),
  scaled down otherwise.
- **Experience Match** = 100 if years of experience meet or exceed the JD
  requirement, scaled proportionally otherwise, 0 for "Fresher" resumes
  when experience is required.

## 5. Ranking
Candidates are sorted in descending order of Final Score.

## 6. LLM Explanation
Separately, the Groq LLM (`llm.py`) reads the same Job Description and
resume text and produces a plain-language summary: strengths, weaknesses,
and a hiring recommendation (Strongly Recommended / Recommended / Consider
/ Not Recommended). This text is descriptive only — it does not affect the
numeric ranking, keeping the ranking measurable and reproducible while the
LLM output stays interpretable.

## Known Limitations
- Skill, education, and experience extraction rely on keyword matching,
  not full resume parsing — unconventional resume formats may be scored
  less accurately.
- Experience detection looks for explicit "X years" phrasing; resumes that
  imply experience without stating a number will be scored as "Fresher".
