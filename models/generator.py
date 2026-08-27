import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY missing from .env")

client = genai.Client(api_key=api_key)

RESUME_SYSTEM_PROMPT = """You are an expert ATS Resume Specialist.
Tailor the candidate's profile to align with the target job description.
Do NOT hallucinate fake credentials. Emphasize matching skills using strong action verbs.
Structure the output in clean Markdown."""

COVER_LETTER_SYSTEM_PROMPT = """You are an expert Career Consultant.
Write a compelling, tailored cover letter based on the candidate's profile and job description.
Maintain a professional tone and keep the length between 250 and 400 words."""


def generate_resume(user_profile: str, job_description: str, temperature: float = 0.3) -> str:
    prompt_text = (
        f"Candidate Profile:\n{user_profile}\n\n"
        f"Target Job Description:\n{job_description}\n\n"
        "Generate the tailored resume in Markdown:"
    )
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt_text,
        config=types.GenerateContentConfig(
            system_instruction=RESUME_SYSTEM_PROMPT,
            temperature=temperature,  # <--- uses the passed temperature parameter
        ),
    )
    return response.text or ""


def generate_cover_letter(user_profile: str, job_description: str, temperature: float = 0.5) -> str:
    prompt_text = (
        f"Candidate Profile:\n{user_profile}\n\n"
        f"Target Job Description:\n{job_description}\n\n"
        "Generate the tailored cover letter:"
    )
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt_text,
        config=types.GenerateContentConfig(
            system_instruction=COVER_LETTER_SYSTEM_PROMPT,
            temperature=temperature,  # <--- uses the passed temperature parameter
        ),
    )
    return response.text or ""