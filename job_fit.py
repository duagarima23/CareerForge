from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def analyze_job_fit(resume_text, job_description):
    prompt = f"""
You are an AI assistant that evaluates how well a resume fits a job description.

Rate the match between the following resume and job description across the following 5 categories (score each from 0 to 100):
1. Skills Match
2. Tools & Technologies Match
3. Experience Match
4. Language & Tone Alignment
5. Overall Fit Score

Then give 1-2 line feedback for each.

Resume:
{resume_text}

Job Description:
{job_description}

Respond in the following JSON format:
{{
  "Skills Match": {{
    "score": number,
    "comment": string
  }},
  "Tools & Technologies Match": {{
    "score": number,
    "comment": string
  }},
  "Experience Match": {{
    "score": number,
    "comment": string
  }},
  "Language & Tone Alignment": {{
    "score": number,
    "comment": string
  }},
  "Overall Fit Score": {{
    "score": number,
    "comment": string
  }}
}}
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )

    import json
    try:
        parsed = json.loads(response.choices[0].message.content.strip())
        return parsed
    except Exception as e:
        return {"error": "Failed to parse job fit score. Please try again.", "details": str(e)}
