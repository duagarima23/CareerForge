from resume_parser import parse_resume
import re


# -------------------------------
# Skill Aliases (Normalization)
# -------------------------------
SKILL_ALIASES = {
    # ML
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",

    # BI
    "powerbi": "power bi",

    # LLM
    "llms": "llm",
    "large language models": "llm",

    # JavaScript
    "js": "javascript",

    # TensorFlow
    "tf": "tensorflow",

    # NLP
    "natural language processing": "nlp",

    # GitHub
    "git hub": "github",

    # GenAI
    "gen ai": "generative ai",
    "genai": "generative ai",

    # Computer Vision
    "computer vision": "opencv"
}


def normalize_skill(skill):
    return SKILL_ALIASES.get(skill.lower().strip(), skill.lower().strip())


# -------------------------------
# Extract Skills from JD
# -------------------------------
def extract_skills_from_jd(jd_text):

    jd_text = jd_text.lower()

    common_skills = [

        # Programming Languages
        "python", "java", "c++", "c", "c#", "javascript",
        "typescript", "go", "ruby", "r", "scala",
        "bash", "shell scripting", "kotlin",
        "swift", "php", "sql", "html", "css",

        # Data Science
        "excel", "pandas", "numpy", "matplotlib",
        "seaborn", "scikit-learn", "power bi",
        "tableau", "data analysis",
        "data visualization",
        "data cleaning",
        "statistics",
        "data mining",
        "exploratory data analysis",
        "business intelligence",

        # AI
        "machine learning",
        "deep learning",
        "tensorflow",
        "keras",
        "nlp",
        "computer vision",
        "neural networks",
        "natural language processing",
        "opencv",
        "huggingface",
        "llm",
        "llms",
        "generative ai",
        "prompt engineering",
        "rag",

        # Web
        "react",
        "angular",
        "vue",
        "node.js",
        "express",
        "django",
        "flask",
        "bootstrap",
        "jquery",
        "frontend",
        "backend",
        "api development",
        "full stack development",

        # DevOps
        "docker",
        "kubernetes",
        "jenkins",
        "git",
        "github",
        "bitbucket",
        "ci/cd",
        "aws",
        "azure",
        "gcp",
        "linux",
        "terraform",
        "ansible",

        # Cybersecurity
        "cybersecurity",
        "network security",
        "penetration testing",
        "ethical hacking",
        "security analysis",
        "firewalls",
        "risk assessment",

        # Project Management
        "project management",
        "agile",
        "scrum",
        "kanban",
        "jira",
        "confluence",
        "product management",
        "roadmapping",
        "requirement analysis",

        # Soft Skills
        "communication",
        "teamwork",
        "leadership",
        "problem solving",
        "critical thinking",
        "collaboration",
        "adaptability",
        "time management",

        # Finance
        "accounting",
        "finance",
        "financial modeling",
        "investment analysis",
        "risk management",
        "business strategy",
        "market research",
        "economics",

        # Design
        "photoshop",
        "illustrator",
        "figma",
        "adobe xd",
        "ui/ux",
        "graphic design",
        "video editing",
        "animation",
        "canva",
        "creativity"
    ]

    jd_skills = []

    for skill in common_skills:

        # Special handling for short language names
        if skill == "c":
            pattern = r"\bc language\b|\bc programming\b|\bc\b"

        elif skill == "r":
            pattern = r"\br language\b|\br programming\b|\br\b"

        elif skill == "go":
            pattern = r"\bgo language\b|\bgolang\b|\bgo\b"

        else:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, jd_text):
            jd_skills.append(normalize_skill(skill))

    return sorted(set(jd_skills))


# -------------------------------
# Compare Resume & JD Skills
# -------------------------------
def compare_skills(resume_skills, jd_skills):

    resume_skills_clean = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    jd_skills_clean = {
        normalize_skill(skill)
        for skill in jd_skills
    }

    matched = sorted(resume_skills_clean & jd_skills_clean)
    missing = sorted(jd_skills_clean - resume_skills_clean)

    score = (
        round((len(matched) / len(jd_skills_clean)) * 100)
        if jd_skills_clean
        else 0
    )

    return matched, missing, score


# -------------------------------
# Test
# -------------------------------
if __name__ == "__main__":

    resume = parse_resume("data/sample_resume.pdf")

    resume_skills = resume["Skills"]

    jd_text = """
    We are looking for a Data Analyst with experience in Python,
    SQL, Excel, Pandas, Power BI, AWS, Docker,
    Machine Learning and Data Visualization.
    """

    jd_skills = extract_skills_from_jd(jd_text)

    matched, missing, score = compare_skills(
        resume_skills,
        jd_skills
    )

    print("\nResume Skills:", resume_skills)
    print("\nJD Skills:", jd_skills)
    print("\nMatched:", matched)
    print("\nMissing:", missing)
    print(f"\nSkill Match Score: {score}%")
