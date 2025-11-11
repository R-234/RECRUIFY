import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from utils.extraction import extract_text
from utils.ai_analysis import get_ai_analysis
from utils.ocr import setup_tesseract

# Setup OCR once
setup_tesseract()

st.set_page_config(page_title="AI Resume Screener", layout="centered")
st.title("AI Resume Screener & Matcher")
st.caption("Zero-cost • Gemini 1.5 Flash • OCR Supported • Top 10 Ranked")

# === UI ===
col1, col2 = st.columns(2)
with col1:
    jd_file = st.file_uploader("Job Description (JD)", type=["pdf", "docx", "txt", "jpg", "png"])
with col2:
    cv_files = st.file_uploader("Candidate CVs", type=["pdf", "docx", "txt", "jpg", "png"], accept_multiple_files=True)

if st.button("Analyze All CVs", type="primary", use_container_width=True):
    if not jd_file or not cv_files:
        st.error("Please upload JD and at least one CV.")
        st.stop()

    with st.spinner("Reading Job Description..."):
        jd_text = extract_text(jd_file)
        if len(jd_text) < 50:
            st.error("JD text too short. Try better scan or paste text.")
            st.stop()

    st.success("JD loaded!")

    progress = st.progress(0)
    results = []

    for i, cv_file in enumerate(cv_files):
        with st.spinner(f"Analyzing {cv_file.name}..."):
            cv_text = extract_text(cv_file)
            result = get_ai_analysis(jd_text, cv_text, cv_file.name)
            results.append(result)
            progress.progress((i + 1) / len(cv_files))

    # Rank & Display
    ranked = sorted(results, key=lambda x: x["match_score"], reverse=True)[:10]
    st.balloons()
    st.success(f"Done! Top {len(ranked)} Candidates")

    for rank, cand in enumerate(ranked, 1):
        with st.expander(f"#{rank} • {cand['filename']} • **{cand['match_score']}/100**", expanded=rank<=3):
            st.write(cand["summary"])
            c1, c2, c3 = st.columns(3)
            c1.metric("Skills", cand["analysis_breakdown"]["skills_score"])
            c2.metric("Experience", cand["analysis_breakdown"]["experience_score"])
            c3.metric("Education", cand["analysis_breakdown"]["education_score"])

            col1, col2 = st.columns(2)
            with col1:
                st.success("Key Matches")
                for m in cand["key_matches"]:
                    st.write(f"• {m}")
            with col2:
                st.warning("Potential Gaps")
                for g in cand["potential_gaps"]:
                    st.write(f"• {g}")