import sys
import traceback
from pathlib import Path

# Ensure root directory is in sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.generator import generate_resume, generate_cover_letter

app = FastAPI(title="AI Resume & Cover Letter Generator API")

class GenerationRequest(BaseModel):
    user_profile: str
    job_description: str

class GenerationResponse(BaseModel):
    resume: str
    cover_letter: str

@app.post("/api/generate", response_model=GenerationResponse)
async def handle_generation(payload: GenerationRequest):
    if not payload.user_profile.strip() or not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="User profile and Job description cannot be empty.")
    
    try:
        res = generate_resume(payload.user_profile, payload.job_description)
        cov = generate_cover_letter(payload.user_profile, payload.job_description)
        return GenerationResponse(resume=res, cover_letter=cov)
    except Exception as e:
        print("\n--- ERROR IN GENERATION ---")
        traceback.print_exc()
        print("----------------------------\n")
        raise HTTPException(status_code=500, detail=str(e))