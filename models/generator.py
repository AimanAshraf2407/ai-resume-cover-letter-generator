import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load variables from .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY was not found. Please check your .env file.")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

# Prompts
RESUME_SYSTEM_PROMPT = (
    "You are an expert ATS resume specialist. Given a candidate profile and a job description, "
    "generate a tailored, professional resume in Markdown format. Emphasize relevant skills and accomplishments."
)

COVER_LETTER_SYSTEM_PROMPT = (
    "You are an expert career consultant. Given a candidate profile and a job description, "
    "generate a compelling, formal cover letter tailored to the target role."
)

def generate_resume(user_profile: str, job_description: str) -> str:
    prompt_text = (
        f"Candidate Profile:\n{user_profile}\n\n"
        f"Target Job Description:\n{job_description}\n\n"
        "Generate the tailored resume in Markdown:"
    )
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",  # <--- Updated to gemini-3.6-flash
        contents=prompt_text,
        config=types.GenerateContentConfig(
            system_instruction=RESUME_SYSTEM_PROMPT,
            temperature=0.4,
        ),
    )
    return response.text or ""


def generate_cover_letter(user_profile: str, job_description: str) -> str:
    prompt_text = (
        f"Candidate Profile:\n{user_profile}\n\n"
        f"Target Job Description:\n{job_description}\n\n"
        "Generate the tailored cover letter:"
    )
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",  # <--- Updated to gemini-3.6-flash
        contents=prompt_text,
        config=types.GenerateContentConfig(
            system_instruction=COVER_LETTER_SYSTEM_PROMPT,
            temperature=0.6,
        ),
    )
    return response.text or ""