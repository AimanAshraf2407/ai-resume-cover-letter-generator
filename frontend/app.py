import os
import streamlit as st
import requests
import json
from pathlib import Path
import sys
import os
API_BASE_URL = os.getenv("API_BASE_URL", "https://your-api.onrender.com")

# Ensure root directory is accessible for local imports
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.exporter import export_to_pdf, export_to_text
from src.evaluation import calculate_ats_metrics

# Fetch backend URL from Streamlit Cloud Secrets, OS Environment, or default to local
if "API_BASE_URL" in st.secrets:
    API_BASE_URL = st.secrets["API_BASE_URL"]
else:
    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="AI Resume & Cover Letter Generator", layout="wide")

st.title("📄 AI Resume & Cover Letter Generator")
st.caption("Powered by Google Gemini 3.6 Flash & FastAPI")

# Initialize session storage for persistent generation state
if "resume" not in st.session_state:
    st.session_state["resume"] = ""
if "cover_letter" not in st.session_state:
    st.session_state["cover_letter"] = ""
if "metrics" not in st.session_state:
    st.session_state["metrics"] = None

# --- SIDEBAR STATUS ---
with st.sidebar:
    st.header("⚙️ Backend Status")
    try:
        health = requests.get(f"{API_BASE_URL}/", timeout=2)
        if health.status_code == 200:
            st.success("🟢 FastAPI Connected (Port 8000)")
        else:
            st.warning("🟡 Backend Status Not OK")
    except requests.exceptions.RequestException:
        st.error("🔴 Backend Offline\nRun: `uvicorn app.main:app --reload --port 8000`")

# --- UI INPUT FIELDS ---
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("1. Candidate Profile")
    name = st.text_input("Full Name", value="Alex Chen")
    email = st.text_input("Email", value="alex.chen@example.com")
    phone = st.text_input("Phone Number", value="+60 12-345 6789")
    linkedin = st.text_input("LinkedIn Profile URL", value="linkedin.com/in/alexchen")
    
    education = st.text_area("Education", value="B.Sc. in Computer Science - University (2026)", height=70)
    experience = st.text_area("Work Experience", value="- Backend Intern at Cloud Solutions (2025): Developed microservices with Python and FastAPI.\n- Built Docker containers and CI/CD pipelines.", height=110)
    skills = st.text_area("Key Skills", value="Python, FastAPI, Docker, PostgreSQL, REST APIs, Git, Linux", height=70)

    st.subheader("2. Target Job Description")
    job_description = st.text_area("Paste Job Requirements", value="We are looking for a Junior AI/Software Engineer proficient in Python, FastAPI, and Docker. Experience integrating Large Language Models and building RESTful APIs is preferred.", height=110)

    st.subheader("3. Select Action")
    doc_selection = st.radio(
        "Choose document to generate:",
        ["Resume Only (T=0.2)", "Cover Letter Only (T=0.7)"],
        horizontal=True
    )

    generate_button = st.button("🚀 Generate Document", type="primary", use_container_width=True)

with col2:
    st.subheader("4. Generated Outputs & ATS Metrics")

    if generate_button:
        if not name.strip() or not job_description.strip():
            st.warning("Please provide at least your Name and the Job Description.")
        else:
            profile_payload = {
                "name": name,
                "email": email,
                "phone": phone,
                "linkedin": linkedin,
                "education": education,
                "experience": experience,
                "skills": skills
            }
            profile_str = json.dumps(profile_payload, indent=2)
            target_type = "resume" if "Resume" in doc_selection else "cover_letter"

            with st.spinner(f"Generating tailored {target_type.replace('_', ' ')} via Gemini 3.6 Flash (~10–15s)..."):
                try:
                    resp = requests.post(
                        f"{API_BASE_URL}/api/generate",
                        json={
                            "user_profile": profile_str,
                            "job_description": job_description,
                            "document_type": target_type
                        },
                        timeout=90
                    )

                    if resp.status_code == 200:
                        data = resp.json()
                        if target_type == "resume":
                            st.session_state["resume"] = data.get("resume", "")
                            # Run ATS evaluation specifically on the generated resume
                            st.session_state["metrics"] = calculate_ats_metrics(
                                profile_str, job_description, st.session_state["resume"]
                            )
                        else:
                            st.session_state["cover_letter"] = data.get("cover_letter", "")

                        st.success(f"Successfully generated {target_type.replace('_', ' ')}!")
                    else:
                        st.error(f"Backend error ({resp.status_code}): {resp.text}")

                except requests.exceptions.ReadTimeout:
                    st.error("Request timed out. Please wait 15–20s for the rate limit bucket to reset, then retry.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to FastAPI. Ensure Uvicorn is running on port 8000.")
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")

    # Show ATS evaluation metrics if a resume exists
    if st.session_state.get("metrics"):
        m = st.session_state["metrics"]
        st.markdown("#### 📊 ATS Keyword Alignment (Resume)")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("ATS Match (Recall)", f"{m.get('keyword_recall_pct', 0)}%")
        m2.metric("Precision", f"{m.get('keyword_precision_pct', 0)}%")
        m3.metric("F1 Score", f"{m.get('f1_score', 0)}")
        m4.metric("Job Keywords", m.get("matched_job_keywords", 0))
        st.markdown("---")

    # Display tab views
    tab_res, tab_cov = st.tabs(["📄 Tailored Resume", "✉️ Cover Letter"])

    with tab_res:
        if st.session_state["resume"]:
            st.markdown(st.session_state["resume"])
            d1, d2 = st.columns(2)
            with d1:
                st.download_button(
                    label="⬇️ Download Resume (.txt)",
                    data=st.session_state["resume"],
                    file_name="tailored_resume.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with d2:
                pdf_path = Path("tailored_resume.pdf")
                export_to_pdf(st.session_state["resume"], pdf_path, title="Tailored Resume")
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Resume (.pdf)",
                        data=f.read(),
                        file_name="tailored_resume.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        else:
            st.info("No resume generated yet. Select **Resume Only** and click Generate.")

    with tab_cov:
        if st.session_state["cover_letter"]:
            st.markdown(st.session_state["cover_letter"])
            d3, d4 = st.columns(2)
            with d3:
                st.download_button(
                    label="⬇️ Download Cover Letter (.txt)",
                    data=st.session_state["cover_letter"],
                    file_name="cover_letter.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with d4:
                cov_pdf_path = Path("cover_letter.pdf")
                export_to_pdf(st.session_state["cover_letter"], cov_pdf_path, title="Cover Letter")
                with open(cov_pdf_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Cover Letter (.pdf)",
                        data=f.read(),
                        file_name="cover_letter.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        else:
            st.info("No cover letter generated yet. Select **Cover Letter Only** and click Generate.")