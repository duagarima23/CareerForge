import PyPDF2
import re


def extract_text_from_pdf(file_path):
    """Extracts all text from a PDF resume."""
    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print(f"Error reading PDF: {e}")

    return text


def extract_email(text):
    """Extract email address from resume."""
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "Email not found"


def extract_phone(text):
    """Extract Indian phone number."""
    match = re.search(r'(\+91[-\s]?)?[6-9]\d{9}', text)
    return match.group(0) if match else "Phone not found"


def extract_name(text):
    """Extract probable name from first few lines."""

    lines = text.split("\n")

    ignore_words = [
        "email", "@", "phone", "contact", "resume",
        "linkedin", "github", "portfolio", "objective"
    ]

    for line in lines[:10]:
        line = line.strip()

        if (
            line
            and len(line.split()) <= 4
            and not any(word in line.lower() for word in ignore_words)
        ):
            return line

    return "Name not found"


def extract_skills(text):
    """Extract technical skills using keyword matching."""

    common_skills = [

        # Programming Languages
        "python", "java", "c", "c++", "javascript",
        "typescript", "r", "go",

        # Databases
        "sql", "mysql", "postgresql", "mongodb", "sqlite",

        # Machine Learning
        "machine learning",
        "deep learning",
        "data science",
        "data analysis",
        "statistics",
        "predictive modeling",
        "tensorflow",
        "keras",
        "pytorch",
        "scikit-learn",
        "xgboost",
        "lightgbm",
        "catboost",

        # NLP & GenAI
        "nlp",
        "generative ai",
        "llm",
        "transformers",
        "huggingface",
        "langchain",
        "langgraph",
        "prompt engineering",
        "rag",

        # Python Libraries
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scipy",
        "opencv",

        # Web Frameworks
        "streamlit",
        "flask",
        "fastapi",
        "django",

        # BI Tools
        "power bi",
        "tableau",
        "excel",

        # Cloud & DevOps
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",
        "git",
        "github",

        # Big Data
        "spark",
        "hadoop",
        "kafka",

        # Miscellaneous
        "linux",
        "rest api"
    ]

    text = text.lower()

    found = []

    for skill in common_skills:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'

        if re.search(pattern, text):
            found.append(skill)

    found = sorted(set(found))

    return found if found else ["Skills not found"]


def parse_resume(file_path):
    """Parse resume and return structured information."""

    text = extract_text_from_pdf(file_path)

    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text),
        "RawText": text
    }


# Test
if __name__ == "__main__":
    path = "data/sample_resume.pdf"

    result = parse_resume(path)

    print("\nResume Details\n")

    for key, value in result.items():
        print(f"{key}: {value}")
