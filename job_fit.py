from openai import OpenAI
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# ✅ Helper function to safely extract JSON
def extract_json(text):
    if not text or not text.strip():
        raise ValueError("Empty response from model")

    text = text.strip()

    # Remove markdown code blocks if present
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    # Try direct parsing
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON from text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError("No valid JSON found")


def analyze_job_fit(resume_text, job_description):
    prompt = f"""
You are an AI assistant that evaluates how well a resume fits a job description.

Rate the match across these 5 categories (0 to 100):
1. Skills Match
2. Tools & Technologies Match
3. Experience Match
4. Language & Tone Alignment
5. Overall Fit Score

Give a short 1-2 line comment for each.

Return ONLY valid JSON.
No explanation, no markdown, no extra text.

Format:
{{
  "Skills Match": {{"score": 0, "comment": "text"}},
  "Tools & Technologies Match": {{"score": 0, "comment": "text"}},
  "Experience Match": {{"score": 0, "comment": "text"}},
  "Language & Tone Alignment": {{"score": 0, "comment": "text"}},
  "Overall Fit Score": {{"score": 0, "comment": "text"}}
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""

    try:
        response = client.chat.completions.create(
            # ✅ FIX 1: stable model
            model="mistralai/mistral-7b-instruct",

            # ✅ FIX 2: system message for strict JSON
            messages=[
                {
                    "role": "system",
                    "content": "Return ONLY valid JSON. No text, no markdown."
                },
                {"role": "user", "content": prompt}
            ],

            # ✅ FIX 3: lower randomness
            temperature=0.3,
            max_tokens=800
        )

        content = response.choices[0].message.content

        # ✅ FIX 4: handle empty response
        if not content or content.strip() == "":
            return {
                "error": "Empty response from model",
                "details": "Check API key / model / quota"
            }

        # DEBUG (optional - remove later)
        print("RAW RESPONSE:", content)

        parsed = extract_json(content)
        return parsed

    except Exception as e:
        return {
            "error": "Failed to parse job fit score. Please try again.",
            "details": str(e)
        }
