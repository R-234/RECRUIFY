
import google.generativeai as genai
import json
import os
from pathlib import Path

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

PROMPT_TEMPLATE = Path("config/prompt.txt").read_text()

def get_ai_analysis(jd_text: str, cv_text: str, filename: str):
    try:
        prompt = PROMPT_TEMPLATE.format(jd_text=jd_text, cv_text=cv_text)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        json_str = response.text.strip().removeprefix("```json").removesuffix("```")
        data = json.loads(json_str)
        data["filename"] = filename
        return data
    except Exception as e:
        return {
            "filename": filename,
            "match_score": 0,
            "summary": f"AI Error: {str(e)}",
            "analysis_breakdown": {"skills_score": "0/50", "experience_score": "0/40", "education_score": "0/10"},
            "key_matches": [], "potential_gaps": ["AI analysis failed."]
        }