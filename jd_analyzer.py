from resume_parser import parse_resume
import re

def extract_skills_from_jd(jd_text):
    jd_text = jd_text.lower()
    common_skills = ['python', 'java', 'sql', 'excel', 'machine learning', 'deep learning', 'tensorflow',
                     'keras', 'nlp', 'data analysis', 'pandas', 'numpy', 'power bi', 'streamlit']
    jd_skills = [skill for skill in common_skills if skill in jd_text]
    return jd_skills

def compare_skills(resume_skills, jd_skills):
    matched = set(resume_skills).intersection(set(jd_skills))
    missing = set(jd_skills).difference(set(resume_skills))
    score = round((len(matched) / len(jd_skills)) * 100) if jd_skills else 0
    return matched, missing, score

if __name__ == "__main__":
    # Load resume data
    resume = parse_resume("data/sample_resume.pdf")
    resume_skills = resume["Skills"]

    # Paste a sample job description here:
    jd_text = """
    We are looking for a Data Analyst with experience in Python, SQL, Excel, Pandas and Power BI.
    The candidate should have a good understanding of data visualization and basic machine learning.
    """

    jd_skills = extract_skills_from_jd(jd_text)
    matched, missing, score = compare_skills(resume_skills, jd_skills)

    print(f"\nResume Skills: {resume_skills}")
    print(f"JD Skills: {jd_skills}")
    print(f"✅ Matched Skills: {matched}")
    print(f"❌ Missing Skills: {missing}")
    print(f"🔍 Skill Match Score: {score}%")

