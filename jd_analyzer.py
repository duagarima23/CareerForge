from resume_parser import parse_resume
import re

def extract_skills_from_jd(jd_text):
    jd_text = jd_text.lower()
    common_skills = [
    # ✅ Programming Languages
    'python', 'java', 'c++', 'c', 'c#', 'javascript', 'typescript', 'go', 'ruby', 'r', 'scala',
    'bash', 'shell scripting', 'kotlin', 'swift', 'php', 'sql', 'html', 'css',

    # 📊 Data Science & Analytics
    'excel', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit-learn', 'power bi', 'tableau',
    'data analysis', 'data visualization', 'data cleaning', 'statistics', 'data mining',
    'exploratory data analysis', 'business intelligence',

    # 🧠 AI & Machine Learning
    'machine learning', 'deep learning', 'tensorflow', 'keras', 'nlp', 'computer vision',
    'neural networks', 'natural language processing', 'opencv', 'huggingface', 'llms',

    # 💻 Web Development
    'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'bootstrap', 'jquery',
    'web development', 'frontend', 'backend', 'api development', 'full stack development',

    # 🛠 DevOps & Cloud
    'docker', 'kubernetes', 'jenkins', 'git', 'github', 'bitbucket', 'ci/cd', 'aws', 'azure',
    'gcp', 'linux', 'terraform', 'ansible',

    # 🔐 Cybersecurity
    'cybersecurity', 'network security', 'penetration testing', 'ethical hacking',
    'security analysis', 'firewalls', 'risk assessment',

    # 🗂 Project & Product Management
    'project management', 'agile', 'scrum', 'kanban', 'jira', 'confluence', 'product management',
    'roadmapping', 'requirement analysis',

    # 🧑‍💼 Soft Skills
    'communication', 'teamwork', 'leadership', 'problem solving', 'critical thinking',
    'collaboration', 'adaptability', 'time management',

    # 🧾 Business & Finance
    'accounting', 'finance', 'financial modeling', 'investment analysis', 'risk management',
    'business strategy', 'market research', 'economics',

    # 🎨 Design & Creative
    'photoshop', 'illustrator', 'figma', 'adobe xd', 'ui/ux', 'graphic design',
    'video editing', 'animation', 'canva', 'creativity'
]

    jd_skills = [skill for skill in common_skills if skill in jd_text]
    return jd_skills

def compare_skills(resume_skills, jd_skills):
    resume_skills_clean = {s.strip().lower() for s in resume_skills}
    jd_skills_clean = {s.strip().lower() for s in jd_skills}

    matched = list(resume_skills_clean & jd_skills_clean)
    missing = list(jd_skills_clean - resume_skills_clean)
    score = int(len(matched) / len(jd_skills_clean) * 100) if jd_skills_clean else 0

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

