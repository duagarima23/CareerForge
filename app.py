import streamlit as st
import os
import time
from resume_critic import critique_resume
from resume_parser import parse_resume
from job_fit import analyze_job_fit
from jd_analyzer import extract_skills_from_jd, compare_skills
from cover_letter_gen import generate_cover_letter
from email_utils import send_email
from interview_bot import generate_interview_questions, give_feedback
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter as LETTER_SIZE
from reportlab.lib.utils import simpleSplit

load_dotenv()
st.set_page_config(page_title="CareerForge – AI Career Assistant", layout="wide", page_icon="🤖")

# --- Global Styles ---
st.markdown("""
<style>
body {
    font-family: 'Poppins', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, #e6f2ff, #ffffff);
}
h1, h2, h3, h4, h5, h6, .st-emotion-cache-10trblm, .stMarkdown {
    color: #003366 !important;
}
div.stButton > button {
    background-color: #e6f2ff;
    color: #004080;
    font-weight: 600;
    border: 1px solid #b3d1ff;
    border-radius: 8px;
    padding: 0.6em 1em;
}
div.stButton > button:hover {
    background-color: #cce6ff;
}
input, textarea {
    background-color: white !important;
    color: black !important;
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- Session State ---
for key in ["resume_uploaded", "jd_submitted", "active_tool", "job_description"]:
    if key not in st.session_state:
        st.session_state[key] = False if key not in ["active_tool", "job_description"] else None

# --- Header ---
st.markdown("""
<div style='text-align: center;'>
    <img src="https://media.istockphoto.com/id/2074604864/vector/chatbot-smiley-robot-face-icon-with-microphone-and-speech-bubble-vector-thin-line.jpg?s=612x612&w=0&k=20&c=MrqadmP-Eq3o7bXHN4WPbv1v8jrwOyS72O6fNcuNqZw=" style='height: 160px;'>
    <h1 style='font-size: 3rem;'>CareerForge</h1>
    <p style='font-size: 1.1rem; color: #003366;'>Craft Your Career with AI Precision</p>
</div>
""", unsafe_allow_html=True)

# --- Features Section ---
st.markdown("""
<h3 style='text-align: center;'>Features</h3>
<div style='display: flex; justify-content: center; flex-wrap: wrap; gap: 1.5rem;'>
    <div style='max-width: 240px; padding: 1rem; background: #e6f2ff; border-radius: 10px; color: #003366;'>
        <h4>Skill Match</h4>
        <p style='font-size: 0.9rem;'>Match your resume skills against job requirements.</p>
    </div>
    <div style='max-width: 240px; padding: 1rem; background: #e6f2ff; border-radius: 10px; color: #003366;'>
        <h4>Job Fit Score</h4>
        <p style='font-size: 0.9rem;'>AI evaluation of resume vs job description.</p>
    </div>
    <div style='max-width: 240px; padding: 1rem; background: #e6f2ff; border-radius: 10px; color: #003366;'>
        <h4>Resume Critique</h4>
        <p style='font-size: 0.9rem;'>Instant feedback on formatting, clarity, and content.</p>
    </div>
    <div style='max-width: 240px; padding: 1rem; background: #e6f2ff; border-radius: 10px; color: #003366;'>
        <h4>Cover Letter Generator</h4>
        <p style='font-size: 0.9rem;'>Generate personalized letters for any job.</p>
    </div>
    <div style='max-width: 240px; padding: 1rem; background: #e6f2ff; border-radius: 10px; color: #003366;'>
        <h4>Interview Q&A</h4>
        <p style='font-size: 0.9rem;'>Answer likely questions and get AI feedback.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Upload Section ---
st.markdown("<h3 style='margin-top:3rem; text-align: center;'>🚀 Get Started</h3>", unsafe_allow_html=True)

if not st.session_state.resume_uploaded:
    uploaded_file = st.file_uploader("Upload your Resume", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        os.makedirs("data", exist_ok=True)
        with open("data/temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.read())
        st.session_state.resume_uploaded = True
        st.success("✅ Resume Uploaded")
else:
    st.info("📎 Resume Uploaded")
    if st.button("🔄 Reset Resume"):
        for key in st.session_state:
            st.session_state[key] = False
        st.rerun()

job_description = st.text_area("Paste Job Description")

if st.button("Submit"):
    if job_description.strip():
        st.session_state.jd_submitted = True
        st.session_state.job_description = job_description
        with st.spinner("⏳ Preparing tools..."):
            time.sleep(1.2)
        st.success("📨 Job Description Submitted!")
    else:
        st.warning("⚠️ Please enter a valid job description.")

# --- Blue Output Box ---
def blue_box(content):
    st.markdown(f"""
    <div style="background-color: #e6f2ff; color: #003366; padding: 1rem 1.2rem; border-radius: 10px; margin-bottom: 1rem;">
        {content}
    </div>
    """, unsafe_allow_html=True)

# --- Tool Section ---
if st.session_state.resume_uploaded and st.session_state.jd_submitted:
    tool_col1, tool_col2, tool_col3, tool_col4, tool_col5 = st.columns(5)
    with tool_col1:
        st.markdown('<span title="Check how well your skills match the job description.">', unsafe_allow_html=True)
        if st.button("🧠 Skill Match"):
            st.session_state.active_tool = "skill_match"
        st.markdown('</span>', unsafe_allow_html=True)
    
    with tool_col2:
        st.markdown('<span title="Visual job fit score using a radar chart.">', unsafe_allow_html=True)
        if st.button("📊 Job Fit Score"):
            st.session_state.active_tool = "job_fit"
        st.markdown('</span>', unsafe_allow_html=True)
    
    with tool_col3:
        st.markdown('<span title="Detailed feedback on your resume formatting, clarity, and content.">', unsafe_allow_html=True)
        if st.button("📋 Resume Critique"):
            st.session_state.active_tool = "resume_critique"
        st.markdown('</span>', unsafe_allow_html=True)
    
    with tool_col4:
        st.markdown('<span title="Generate a professional cover letter for this job.">', unsafe_allow_html=True)
        if st.button("✉️ Cover Letter"):
            st.session_state.active_tool = "cover_letter"
        st.markdown('</span>', unsafe_allow_html=True)
    
    with tool_col5:
        st.markdown('<span title="Practice answering interview questions with AI feedback.">', unsafe_allow_html=True)
        if st.button("🎤 Interview Q&A"):
            st.session_state.active_tool = "interview_qa"
        st.markdown('</span>', unsafe_allow_html=True)


    tool = st.session_state.active_tool

    if tool == "skill_match":
        with st.spinner("Analyzing skill match..."):
            resume_data = parse_resume("data/temp_resume.pdf")
            jd_skills = extract_skills_from_jd(st.session_state.job_description)
            matched, missing, score = compare_skills(resume_data['Skills'], jd_skills)
            content = f"<h4>🎯 Skill Match Score: {score}%</h4><p><strong>✅ Matched Skills:</strong> {', '.join(matched)}</p>"
            if missing:
                content += f"<p><strong>❌ Missing Skills:</strong> {', '.join(missing)}</p>"
            blue_box(content)

    elif tool == "job_fit":
        with st.spinner("Calculating job fit..."):
            resume_data = parse_resume("data/temp_resume.pdf")
            result = analyze_job_fit(resume_data["RawText"], st.session_state.job_description)
            df = pd.DataFrame({"Category": list(result.keys()), "Score": [v["score"] for v in result.values()]})

            def radar_plot():
                N = len(df)
                angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
                values = df['Score'].tolist()
                values += values[:1]
                angles += angles[:1]
                plt.style.use("dark_background")
                fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(polar=True))
                fig.patch.set_facecolor("#111")
                ax.set_facecolor("#111")
                ax.plot(angles, values, color='cyan', linewidth=2)
                ax.fill(angles, values, color='cyan', alpha=0.3)
                ax.set_yticks([20, 40, 60, 80, 100])
                ax.set_yticklabels(['20', '40', '60', '80', '100'], color='gray', fontsize=6)
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(df['Category'].tolist(), color='white', fontsize=7)
                ax.grid(color='gray', linestyle='dashed', linewidth=0.5)
                _, col, _ = st.columns([4, 2, 4])
                with col:
                    st.pyplot(fig)
            radar_plot()

            for cat, info in result.items():
                blue_box(f"<strong>{cat}</strong>: {info['score']}%<br><em>{info['comment']}</em>")

    elif tool == "resume_critique":
        with st.spinner("Reviewing resume..."):
            resume_data = parse_resume("data/temp_resume.pdf")
            feedback = critique_resume(resume_data)
            blue_box(f"<h4>📋 Resume Critique</h4><p>{feedback}</p>")

    elif tool == "cover_letter":
        with st.spinner("Writing cover letter..."):
            resume_data = parse_resume("data/temp_resume.pdf")
            resume_summary = f"{resume_data['Name']} has skills in {', '.join(resume_data['Skills'])}. Contact: {resume_data['Email']} | {resume_data['Phone']}"
            letter = generate_cover_letter(resume_summary, st.session_state.job_description)
            blue_box(f"<h4>✉️ Generated Cover Letter</h4><pre>{letter}</pre>")

    elif tool == "interview_qa":
        with st.spinner("Generating questions..."):
            resume_data = parse_resume("data/temp_resume.pdf")
            resume_summary = f"{resume_data['Name']} has skills in {', '.join(resume_data['Skills'])}. Contact: {resume_data['Email']} | {resume_data['Phone']}"
            questions = generate_interview_questions(resume_summary, st.session_state.job_description)
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}: {q}**")
                a = st.text_area("Your Answer", key=f"ans_{i}")
                if st.button(f"💬 Feedback for Q{i+1}", key=f"fb_{i}"):
                    if a:
                        fb = give_feedback(q, a)
                        blue_box(f"<strong>Feedback:</strong> {fb}")
                    else:
                        st.warning("Please provide your answer first.")

# --- Footer ---
st.markdown("""
<hr style="margin-top: 3rem;">
<div style='text-align: center; color: gray;'>Made with ❤️ by Garima | CareerForge 2025</div>
""", unsafe_allow_html=True)
