"""
Resume Screening Agent - Streamlit Frontend
Reuses existing backend modules: parser, jd_parser, extractor, scorer, llm, exporter.
No backend scoring logic is changed here (bug fixes were made directly in
extractor.py, jd_parser.py, and scorer.py).

The Job Description is fixed (Data Scientist role, see jd.txt) - no JD upload.
Resumes can be screened using the 10 bundled sample resumes, or the user's own
uploads (max 10).
"""

import os
import json
import tempfile

import streamlit as st
import pandas as pd
import plotly.express as px

from parser import extract_text
from jd_parser import parse_job_description
from extractor import extract_resume_info
from scorer import calculate_final_score
from llm import analyze_resume
from exporter import export_results

MAX_RESUMES = 10
SUPPORTED_EXTENSIONS = (".pdf", ".docx", ".txt")
JD_FILE = "jd.txt"
SAMPLE_RESUME_FOLDER = "resumes"

# -----------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="Resume Screening Agent",
    page_icon="🧑‍💼",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main { background-color: #FFFFFF; }
    .top-card {
        background-color: #0B3D91;
        color: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------
if "results" not in st.session_state:
    st.session_state.results = None
if "resume_files" not in st.session_state:
    st.session_state.resume_files = []

# -----------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------
def get_recommendation(score):
    if score >= 75:
        return "Strong Fit"
    elif score >= 50:
        return "Moderate Fit"
    else:
        return "Weak Fit"


def save_uploaded_file(uploaded_file, folder):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def is_supported(filename):
    return filename.lower().endswith(SUPPORTED_EXTENSIONS)


@st.cache_data
def load_jd_text():
    with open(JD_FILE, "r", encoding="utf-8") as f:
        return f.read()


def list_sample_resumes():
    return sorted(
        f for f in os.listdir(SAMPLE_RESUME_FOLDER) if is_supported(f)
    )


# -----------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------
with st.sidebar:
    st.header("📋 Project Info")
    st.markdown(
        "**Resume Screening Agent**\n\n"
        "AI-powered candidate ranking system that compares resumes "
        "against a fixed Job Description using semantic similarity, "
        "skill matching, and LLM-generated reasoning."
    )

    st.subheader("🛠️ Technology Stack")
    st.markdown(
        "- Python\n"
        "- Groq (LLM)\n"
        "- Sentence Transformers (NLP)\n"
        "- Streamlit\n"
    )

    st.subheader("📁 Resumes Loaded")
    st.write(f"{len(st.session_state.resume_files)} / {MAX_RESUMES}")

    if st.button("🗑️ Clear Uploads"):
        st.session_state.resume_files = []
        st.session_state.results = None
        st.rerun()

# -----------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------
st.title("🧑‍💼 Resume Screening Agent")
st.caption("AI Powered Resume Ranking System")

# -----------------------------------------------------------------------
# Section 1: Job Description (fixed, read-only)
# -----------------------------------------------------------------------
st.subheader("1️⃣ Job Description")
jd_text = load_jd_text()
st.info("This agent screens candidates against a fixed **Data Scientist** role.")
with st.expander("📄 View Job Description"):
    st.text(jd_text)

# -----------------------------------------------------------------------
# Section 2: Resumes
# -----------------------------------------------------------------------
st.subheader("2️⃣ Resumes")

resume_mode = st.radio(
    "Choose resume source",
    ["Use 10 bundled sample resumes", "Upload my own resumes"],
    horizontal=True,
)

if resume_mode == "Use 10 bundled sample resumes":
    sample_names = list_sample_resumes()
    st.session_state.resume_files = [
        {"name": n, "path": os.path.join(SAMPLE_RESUME_FOLDER, n)}
        for n in sample_names
    ]
    st.write(f"Loaded {len(sample_names)} sample resumes:")
    st.write(", ".join(sample_names))

else:
    resume_uploads = st.file_uploader(
        "Upload up to 10 resumes (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="resume_uploader",
    )

    if resume_uploads:
        if len(resume_uploads) > MAX_RESUMES:
            st.warning(
                f"⚠️ You uploaded {len(resume_uploads)} resumes. "
                f"Only the first {MAX_RESUMES} will be processed."
            )
            resume_uploads = resume_uploads[:MAX_RESUMES]

        st.session_state.resume_files = [
            {"name": f.name, "uploaded_file": f} for f in resume_uploads
        ]
        st.write("Uploaded resumes:")
        for f in resume_uploads:
            st.write(f"- {f.name}")
    else:
        st.session_state.resume_files = []

# -----------------------------------------------------------------------
# Section 3: Screen Resumes Button
# -----------------------------------------------------------------------
st.subheader("3️⃣ Run Screening")

resumes_ready = len(st.session_state.resume_files) > 0
if not resumes_ready:
    st.info("Select sample resumes or upload your own to continue.")

run_clicked = st.button("🚀 Screen Resumes", disabled=not resumes_ready)

# -----------------------------------------------------------------------
# Processing
# -----------------------------------------------------------------------
if run_clicked:
    with tempfile.TemporaryDirectory() as temp_dir:

        progress = st.progress(0, text="Extracting job requirements...")
        jd_info = parse_job_description(jd_text)

        results = []
        resume_entries = st.session_state.resume_files
        total = len(resume_entries)

        for i, entry in enumerate(resume_entries):

            name = entry["name"]

            if not is_supported(name):
                st.error(f"Unsupported file format: {name}")
                continue

            step_pct = 10 + int((i / total) * 70)
            progress.progress(step_pct, text=f"Analyzing {name}...")

            try:
                if "path" in entry:
                    resume_path = entry["path"]
                else:
                    resume_path = save_uploaded_file(
                        entry["uploaded_file"], temp_dir
                    )

                resume_text = extract_text(resume_path)
                resume_info = extract_resume_info(resume_text)

                final_score, details = calculate_final_score(
                    jd_info, resume_info, jd_text, resume_text
                )

                explanation = analyze_resume(jd_text, resume_text)

                results.append({
                    "Candidate": name,
                    "Final Score": final_score,
                    "Semantic Score": details["semantic_score"],
                    "Skill Score": details["skill_score"],
                    "Education Score": details["education_score"],
                    "Experience Score": details["experience_score"],
                    "Matched Skills": ", ".join(details["matched_skills"]),
                    "Missing Skills": ", ".join(details["missing_skills"]),
                    "Recommendation": get_recommendation(final_score),
                    "LLM Analysis": explanation,
                })

            except Exception as error:
                st.warning(f"Skipped {name}: {error}")
                continue

        progress.progress(85, text="Ranking candidates...")
        results.sort(key=lambda c: c["Final Score"], reverse=True)
        for idx, candidate in enumerate(results, start=1):
            candidate["Rank"] = idx

        progress.progress(95, text="Exporting results...")
        export_results(results)

        progress.progress(100, text="Done.")
        st.session_state.results = results

    st.success(f"✅ Processed {len(st.session_state.results)} resume(s) successfully.")

# -----------------------------------------------------------------------
# Results Page
# -----------------------------------------------------------------------
results = st.session_state.results

if results:
    st.divider()
    st.header("📊 Results")

    df = pd.DataFrame(results)

    top = results[0]
    st.markdown(
        f"""
        <div class="top-card">
            <h3>🏆 Top Candidate: {top['Candidate']}</h3>
            <p><b>Final Score:</b> {top['Final Score']} / 100</p>
            <p><b>Recommendation:</b> {top['Recommendation']}</p>
            <p><b>Matched Skills:</b> {top['Matched Skills'] or '—'}</p>
            <p><b>Missing Skills:</b> {top['Missing Skills'] or '—'}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.subheader("📋 Ranking Table")
    table_cols = [
        "Rank", "Candidate", "Final Score", "Semantic Score",
        "Skill Score", "Education Score", "Experience Score",
        "Recommendation",
    ]
    st.dataframe(df[table_cols], use_container_width=True, hide_index=True)

    st.subheader("🔍 Candidate Details")
    for candidate in results:
        with st.expander(
            f"Rank {candidate['Rank']} — {candidate['Candidate']} "
            f"({candidate['Final Score']} pts, {candidate['Recommendation']})"
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Matched Skills:** {candidate['Matched Skills'] or '—'}")
                st.markdown(f"**Missing Skills:** {candidate['Missing Skills'] or '—'}")
                st.markdown(f"**Recommendation:** {candidate['Recommendation']}")
            with col2:
                st.markdown(f"**Final Score:** {candidate['Final Score']}")
                st.markdown(f"**Semantic Score:** {candidate['Semantic Score']}")
                st.markdown(f"**Skill Score:** {candidate['Skill Score']}")
                st.markdown(f"**Education Score:** {candidate['Education Score']}")
                st.markdown(f"**Experience Score:** {candidate['Experience Score']}")
            st.markdown("**AI Analysis:**")
            st.text(candidate["LLM Analysis"])

    st.subheader("📈 Visuals")
    vis_col1, vis_col2 = st.columns(2)

    with vis_col1:
        fig_bar = px.bar(
            df.sort_values("Final Score", ascending=True),
            x="Final Score",
            y="Candidate",
            orientation="h",
            title="Candidate Scores",
            color="Final Score",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with vis_col2:
        rec_counts = df["Recommendation"].value_counts().reset_index()
        rec_counts.columns = ["Recommendation", "Count"]
        fig_pie = px.pie(
            rec_counts,
            names="Recommendation",
            values="Count",
            title="Recommendation Distribution",
            color_discrete_sequence=px.colors.sequential.Blues_r,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("⬇️ Downloads")
    dl_col1, dl_col2 = st.columns(2)

    with dl_col1:
        st.download_button(
            "Download CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="ranked_candidates.csv",
            mime="text/csv",
        )

    with dl_col2:
        st.download_button(
            "Download JSON",
            data=json.dumps(results, indent=4, ensure_ascii=False).encode("utf-8"),
            file_name="ranked_candidates.json",
            mime="application/json",
        )
