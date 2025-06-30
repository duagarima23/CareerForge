from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

# ✅ Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# 🔹 Generate Interview Questions
def generate_interview_questions(resume_summary, job_description):
    prompt = f"""
You are a technical interviewer.

Based on the candidate's resume and the job description below, generate 5 relevant interview questions. 
Ask a mix of technical, behavioral, and situational questions. 
Return only the questions — one per line, no explanation or formatting like 'Q1:'.

--- RESUME SUMMARY ---
{resume_summary}

--- JOB DESCRIPTION ---
{job_description}
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",  # You can swap with any OpenRouter model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=600
    )

    output = response.choices[0].message.content.strip()
    questions = [q.strip("•-12345. ").strip() for q in output.split("\n") if q.strip()]
    return questions

# 🔹 Give Feedback on User Answer
def give_feedback(question, user_answer):
    prompt = f"""
You are an expert technical interviewer.

The candidate was asked: "{question}"
Their answer: "{user_answer}"

Give helpful, constructive feedback (2-3 lines) and then suggest an improved or ideal version of the answer.
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=400
    )

    return response.choices[0].message.content.strip()
