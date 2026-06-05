import json
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

def extract_skills_llm(text):

    prompt = f"""
    Extract all skills from this resume.

    Return ONLY JSON.

    {{
      "technical_skills": [],
      "soft_skills": [],
      "tools": [],
      "frameworks": [],
      "certifications": [],
      "domain_expertise": []
    }}

    Resume:

    {text}
    """

    try:

        response = model.generate_content(
            prompt
        )

        result = response.text

        result = result.replace(
            "```json",
            ""
        )

        result = result.replace(
            "```",
            ""
        )

        return json.loads(result)

    except Exception as e:

        return {
            "technical_skills": [],
            "soft_skills": [],
            "tools": [],
            "frameworks": [],
            "certifications": [],
            "domain_expertise": [],
            "error": str(e)
        }
    
    