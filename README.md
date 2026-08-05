# Resume Screening Agent
HEAD
AI-powered resume ranking system. Compares resumes against a fixed
Data Scientist Job Description using NLP semantic similarity, skill
matching, and LLM-generated reasoning, then outputs a ranked shortlist.

## Deliverables (per spec)
- Job Description: `jd.txt` (Data Scientist role, hardcoded — no JD upload needed)
- Sample resumes: `resumes/` (10 pre-loaded resumes, PDF/DOCX/TXT)
- Ranked output: `output/ranked_candidates.csv`, `output/ranked_candidates.json`
- Scoring method note: `SCORING_METHOD.md`

## Capabilities
- Parses PDF / DOCX / TXT resumes
- Extracts skills, education level, and years of experience
- Computes relevance score using sentence-embedding similarity (`all-MiniLM-L6-v2`)
- Ranks candidates with a reasoned explanation per candidate (via Groq LLM)
- Handles 10+ resumes in a single run

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root with your Groq API key:

```
GROQ_API_KEY=your_key_here
```

## Running

**Command line** (processes everything in `resumes/`, writes to `output/`):
```bash
python main.py
```

**Web app**:
```bash
streamlit run app.py
```
By default the app uses the 10 bundled sample resumes. You can switch to
uploading your own resumes (max 10) from the UI.

## Project Structure
```
resume_screening_agent/
├── app.py              # Streamlit frontend
├── main.py             # CLI entry point
├── parser.py           # PDF/DOCX/TXT text extraction
├── jd_parser.py         # Job description parsing
├── extractor.py         # Resume skill/education/experience extraction
├── similarity.py         # Sentence-embedding cosine similarity
├── scorer.py            # Weighted final scoring
├── llm.py               # Groq LLM explanation generation
├── exporter.py           # CSV/JSON export
├── jd.txt               # Fixed Job Description
├── resumes/              # Sample resumes
├── output/               # Generated CSV/JSON
├── SCORING_METHOD.md      # Scoring methodology note
└── requirements.txt
```

## Scoring Method
See `SCORING_METHOD.md` for the full breakdown. Summary:

An AI-powered agent that screens and ranks resumes against a Job Description.
It combines **objective NLP similarity scoring** (sentence embeddings +
weighted skill/education/experience matching) with an **LLM-generated
explanation** for each candidate, then outputs a ranked shortlist as CSV
and JSON.

**One sentence:** This agent takes a Job Description and a folder of
resumes as input, and produces a ranked list of candidates with relevance
scores and explanations.


## 1. Installation

**Requirements:** Python 3.10–3.12 (Python 3.14 has known compatibility
issues with the `protobuf`/`streamlit` dependency chain — use 3.10-3.12).

```bash
git clone <your-repo-url>
cd Resume_screening_agent
pip install -r requirements.txt
```

---

## 2. Configure API Keys

This agent uses [Groq](https://console.groq.com) (free tier) for the
LLM-generated explanation step.

1. Create a free account at console.groq.com
2. Generate an API key
3. Create a file named `.env` in the project root:
   ```
   GROQ_API_KEY=your_key_here
   ```
   (See `.env.example` for the expected format. Never commit your real
   `.env` file — it's excluded via `.gitignore`.)

---

## 3. Run the Agent End to End

### Option A — Web app (recommended)
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`. By default it uses the 10 bundled
sample resumes in `resumes/` against the fixed Job Description in
`jd.txt`. Click **🚀 Screen Resumes** to run the full pipeline. You can
also switch to uploading your own resumes (max 10) from the UI.

### Option B — Command line
```bash
python main.py
```
Processes every resume in `resumes/` against `jd.txt` and writes results
directly to `output/ranked_candidates.csv` and `output/ranked_candidates.json`.

---

## 4. Sample Inputs and Outputs

| Deliverable | Location |
|---|---|
| Job Description | `jd.txt` (Data Scientist role) |
| Sample resumes | `resumes/` (10 resumes, mix of PDF/DOCX/TXT) |
| Ranked output (CSV) | `output/ranked_candidates.csv` (generated after running) |
| Ranked output (JSON) | `output/ranked_candidates.json` (generated after running) |
| Scoring method note | `SCORING_METHOD.md` |

Run the agent once (`main.py` or the app) to populate `output/` with a
real, reproducible ranking of the 10 sample resumes.

---

## 5. Design Choices

- **Hybrid scoring, not LLM-only ranking.** The final rank is computed
  from measurable signals (embedding similarity + skill/education/
  experience matching), not the LLM's subjective judgment. The LLM is
  used only to generate the human-readable explanation. This keeps the
  ranking reproducible and auditable — running the same inputs twice
  gives the same order, which a pure LLM-scoring approach would not
  guarantee.
- **`all-MiniLM-L6-v2` for embeddings.** Small, fast, runs locally with
  no extra API cost, and good enough accuracy for resume/JD semantic
  matching.
- **Groq (`llama-3.1-8b-instant`) for explanations.** Free tier, fast
  inference, sufficient for a summarization/reasoning task that doesn't
  need a frontier model.
- **Education compared by level, not exact text.** Early versions
  compared education strings exactly (`"bachelor" == "b.tech"` → false),
  which silently zeroed out qualified candidates. Fixed to compare
  normalized levels (Bachelor's/Master's/PhD) instead.
- **Fixed Job Description, no JD upload.** Scoped to one role
  (Data Scientist) to keep the demo self-contained and reproducible for
  reviewers without requiring them to supply their own JD.

## Weighting
755f84f4e0b4b84889feadf4a449b2e02847f817
```
Final Score = 0.50 × Semantic Similarity
            + 0.30 × Skill Match
            + 0.10 × Education Match
            + 0.10 × Experience Match
```
HEAD

## Limitations
- Skill/education/experience extraction is keyword-based, not a full resume
  parser — unconventional formats may score less accurately.
- Experience detection requires explicit "X years" phrasing.
- Requires a valid Groq API key for the LLM explanation step.

Full breakdown in `SCORING_METHOD.md`.


## 6. Tradeoffs and Limitations

- **Keyword-based extraction, not a full resume parser.** Skills,
  education, and experience are extracted via keyword/regex matching
  against predefined lists, not a trained NER model. Resumes using
  unconventional phrasing or formats may be scored less accurately.
- **Experience detection requires explicit "X years" phrasing.** A
  resume that lists years worked without that phrasing (e.g. only
  listing employment date ranges) will be scored as "Fresher."
- **No parallelization.** Each resume triggers a sequential Groq API
  call, so processing time scales linearly with the number of resumes
  (roughly 30s-2min for 10 resumes, longer on the very first run while
  the embedding model downloads).
- **Single fixed JD.** Multi-JD or JD-upload support was descoped for
  this submission to keep the demo simple and reproducible.

**What I'd improve with more time:**
- Replace keyword extraction with a lightweight NER model for skills/
  education/experience, to reduce false negatives on non-standard resumes.
- Parallelize LLM calls across resumes to cut total run time.
- Add JD upload back with the fixed JD as a "quick demo" default.
- Add unit tests asserting the weighted formula against known
  hand-scored examples (some test files exist in `test_*.py` but aren't
  wired into CI).


## Project Structure
```
Resume_screening_agent/
├── app.py                # Streamlit frontend
├── main.py                # CLI entry point
├── parser.py               # PDF/DOCX/TXT text extraction
├── jd_parser.py             # Job description parsing
├── extractor.py              # Resume skill/education/experience extraction
├── similarity.py              # Sentence-embedding cosine similarity
├── scorer.py                  # Weighted final scoring
├── llm.py                     # Groq LLM explanation generation
├── exporter.py                 # CSV/JSON export
├── config.py                    # Model names and scoring weights
├── jd.txt                        # Fixed Job Description
├── resumes/                       # 10 sample resumes
├── output/                         # Generated CSV/JSON (after running)
├── SCORING_METHOD.md                # Scoring methodology note
├── .env.example                      # Template for API key config
└── requirements.txt
```
755f84f4e0b4b84889feadf4a449b2e02847f817
