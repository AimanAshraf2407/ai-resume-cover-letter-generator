import streamlit as st
import time

# Page configuration
st.set_page_config(page_title="AI Resume & Cover Letter Generator", layout="wide")

st.title("📄 AI Resume & Cover Letter Generator")
st.caption("Generate tailored resumes and cover letters matched to job descriptions.")

# --- MOCK AI FUNCTION (Person 1 will replace this later) ---
def mock_generate_content(profile_data, job_desc):
    time.sleep(1.5)  # Simulate AI generation latency
    
    resume_output = f"""# {profile_data['name'].upper()}
Contact: {profile_data['email']} | {profile_data['phone']} | {profile_data['linkedin']}

## PROFESSIONAL SUMMARY
Results-driven professional with experience tailored for the target role. Proven ability to apply technical expertise to meet industry standards.

## SKILLS
{profile_data['skills']}

## EXPERIENCE
{profile_data['experience']}

## EDUCATION
{profile_data['education']}
"""

    cover_letter_output = f"""Dear Hiring Team,

I am writing to express my strong interest in the open position. With my background in {profile_data['skills']}, I am confident in my ability to contribute effectively to your organization.

In my previous roles:
{profile_data['experience']}

I am excited about this opportunity and look forward to discussing how my skillset aligns with your team's goals.

Sincerely,
{profile_data['name']}
"""
    return resume_output, cover_letter_output

# --- USER INTERFACE ---
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("1. User Profile Details")
    name = st.text_input("Full Name", value="John Doe")
    email = st.text_input("Email", value="johndoe@example.com")
    phone = st.text_input("Phone Number", value="+60 12-345 6789")
    linkedin = st.text_input("LinkedIn Profile URL", value="linkedin.com/in/johndoe")
    
    education = st.text_area("Education", value="B.Sc. in Computer Science - University (2026)", height=80)
    experience = st.text_area("Work Experience", value="- Software Intern at Tech Corp (2025): Developed features using Python.\n- Freelance Developer: Built small automation tools.", height=120)
    skills = st.text_area("Key Skills", value="Python, Linux, Docker, Git, REST APIs", height=80)

    st.subheader("2. Target Job Details")
    target_job_title = st.text_input("Target Job Title", value="Junior Software Engineer")
    job_description = st.text_area("Job Description (Paste requirements here)", value="Looking for an entry-level software engineer proficient in Python and container concepts...", height=140)

    generate_button = st.button("🚀 Generate Documents", type="primary", use_container_width=True)

with col2:
    st.subheader("3. Generated Documents")
    
    if generate_button:
        if not name or not job_description:
            st.warning("Please fill in at least the Name and Job Description.")
        else:
            with st.spinner("AI is tailoring your resume and cover letter..."):
                profile_payload = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "linkedin": linkedin,
                    "education": education,
                    "experience": experience,
                    "skills": skills,
                    "job_title": target_job_title
                }
                
                # Call the generator function
                gen_resume, gen_cover_letter = mock_generate_content(profile_payload, job_description)
                
                # Store results in session state so they persist across interactions
                st.session_state["resume"] = gen_resume
                st.session_state["cover_letter"] = gen_cover_letter
                st.success("Generation complete!")

    # Display generated results if available in session state
    if "resume" in st.session_state and "cover_letter" in st.session_state:
        tab_resume, tab_cover = st.tabs(["📄 Tailored Resume", "✉️ Cover Letter"])
        
        with tab_resume:
            st.markdown(st.session_state["resume"])
            st.download_button(
                label="📥 Download Resume (.txt)",
                data=st.session_state["resume"],
                file_name="tailored_resume.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        with tab_cover:
            st.markdown(st.session_state["cover_letter"])
            st.download_button(
                label="📥 Download Cover Letter (.txt)",
                data=st.session_state["cover_letter"],
                file_name="cover_letter.txt",
                mime="text/plain",
                use_container_width=True
            )
    else:
        st.info("Fill in the details on the left and click **Generate Documents** to see output here.")