from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.generator import generate_resume, generate_cover_letter

app = FastAPI(
    title="AI Resume & Cover Letter Generator API",
    description="Backend API powered by Google Gemini 3.6 Flash",
    version="1.0.0"
)

class GenerationRequest(BaseModel):
    user_profile: str
    job_description: str

class GenerationResponse(BaseModel):
    resume: str
    cover_letter: str


@app.get("/")
def read_root():
    """Root endpoint health check."""
    return {
        "status": "online",
        "message": "AI Resume & Cover Letter Generator API is running"
    }


@app.post("/api/generate", response_model=GenerationResponse)
def generate_documents(request: GenerationRequest):
    if not request.user_profile.strip() or not request.job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="user_profile and job_description cannot be empty strings."
        )
    
    try:
        resume = generate_resume(
            user_profile=request.user_profile,
            job_description=request.job_description,
            temperature=0.2
        )
        cover_letter = generate_cover_letter(
            user_profile=request.user_profile,
            job_description=request.job_description,
            temperature=0.5
        )
        return GenerationResponse(resume=resume, cover_letter=cover_letter)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))