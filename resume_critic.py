from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def critique_resume(parsed_resume):
    resume_text = parsed_resume["RawText"]
    

    prompt = f"""
You are an expert resume reviewer.

Carefully read the resume content below and provide a structured critique.
Evaluate:
- Section completeness (Education, Experience, Projects, Certifications)
- Clarity and impact of language
- Formatting (based on extracted text)
- Use of keywords and quantifiable achievements

Resume:
{resume_text}

Please return:
1. Strengths (in bullet points)
2. Areas for Improvement (in bullet points)
3. Specific Suggestions (in bullet points)
"""


    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=600
    )

    return response.choices[0].message.content.strip()
