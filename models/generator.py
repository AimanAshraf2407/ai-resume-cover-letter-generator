import os
import re
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError, ClientError

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY missing from .env")

client = genai.Client(api_key=api_key)

# The active model required by the Google GenAI SDK
MODEL_NAME = "gemini-3.6-flash"

RESUME_SYSTEM_PROMPT = """You are an expert ATS Resume Specialist.
Tailor the candidate's profile to align with the target job description.
Do NOT hallucinate fake credentials. Emphasize matching skills using strong action verbs.
Structure the output in clean Markdown."""

COVER_LETTER_SYSTEM_PROMPT = """You are an expert Career Consultant.
Write a compelling, tailored cover letter based on the candidate's profile and job description.
Maintain a professional tone and keep the length between 250 and 400 words."""


def call_gemini_with_retry(prompt: str, system_prompt: str, temperature: float, max_retries: int = 5) -> str:
    """Invokes Gemini 3.6 Flash and handles 429 quota backoffs gracefully."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temperature,
                ),
            )
            return response.text or ""
        except ClientError as e:
            err_msg = str(e)
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                # Extract wait time from error message or default to 30s
                match = re.search(r"retry in (\d+(?:\.\d+)?)s", err_msg)
                wait_sec = float(match.group(1)) + 3.0 if match else 30.0
                print(f"\n⏳ [Free Tier Quota] API requested cooldown. Waiting {wait_sec:.1f}s before retry ({attempt + 1}/{max_retries})...")
                time.sleep(wait_sec)
            else:
                raise e
        except ServerError:
            print(f"\n⏳ [5xx Server Error] Retrying in 10s ({attempt + 1}/{max_retries})...")
            time.sleep(10)

    raise RuntimeError("Generation failed after maximum retry attempts. Rate limit bucket full.")


def generate_resume(user_profile: str, job_description: str, temperature: float = 0.3) -> str:
    prompt_text = (
        f"Candidate Profile:\n{user_profile}\n\n"
        f"Target Job Description:\n{job_description}\n\n"
        "Generate the tailored resume in Markdown:"
    )
    return call_gemini_with_retry(prompt_text, RESUME_SYSTEM_PROMPT, temperature)


def generate_cover_letter(user_profile: str, job_description: str, temperature: float = 0.5) -> str:
    prompt_text = (
        f"Candidate Profile:\n{user_profile}\n\n"
        f"Target Job Description:\n{job_description}\n\n"
        "Generate the tailored cover letter:"
    )
    return call_gemini_with_retry(prompt_text, COVER_LETTER_SYSTEM_PROMPT, temperature)