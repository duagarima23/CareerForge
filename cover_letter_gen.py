from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Initialize client for OpenRouter (GPT alternative)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def generate_cover_letter(resume_summary, job_description):
    prompt = f"""
    Write a personalized, professional cover letter for the following job. Highlight relevant strengths and experience.

    --- RESUME SUMMARY ---
    {resume_summary}

    --- JOB DESCRIPTION ---
    {job_description}

    The tone should be formal and confident. Format it properly.
    """

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",  # Free, fast model
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()

# Example test
if __name__ == "__main__":
    resume_summary = """
    Garima Dua is a Data Analyst with experience in Python, SQL, Pandas, Power BI, and data visualization. She has built dashboards and extracted insights to improve business decisions.
    """

    job_description = """
    We are looking for a Business Analyst to analyze trends and generate reports using Python and Power BI. The role involves collaborating with cross-functional teams and presenting insights to stakeholders.
    """

    letter = generate_cover_letter(resume_summary, job_description)
    print("\n--- COVER LETTER ---\n")
    print(letter)
