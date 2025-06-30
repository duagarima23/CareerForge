import PyPDF2
import re

def extract_text_from_pdf(file_path):
    """Extracts all text from a PDF resume."""
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "Email not found"

def extract_phone(text):
    match = re.search(r'(\+91)?\s?[789]\d{9}', text)
    return match.group(0) if match else "Phone not found"

def extract_name(text):
    lines = text.split("\n")
    for line in lines:
        if line.strip() and not any(x in line.lower() for x in ['email', '@', 'phone', 'contact']):
            return line.strip()
    return "Name not found"

def extract_skills(text):
    common_skills = [
        'python', 'java', 'sql', 'excel', 'machine learning', 'deep learning', 'tensorflow',
        'keras', 'nlp', 'data analysis', 'pandas', 'numpy', 'power bi', 'streamlit'
    ]
    found = [skill for skill in common_skills if skill.lower() in text.lower()]
    return found if found else ["Skills not found"]

def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)

    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text),
        "RawText": text  # ✅ Add full text for AI review
    }

# Optional test
if __name__ == "__main__":
    path = "data/sample_resume.pdf"
    result = parse_resume(path)
    for key, value in result.items():
        print(f"{key}: {value}")
