from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from models.generator import generate_resume, generate_cover_letter

app = FastAPI(
    title="AI Resume & Cover Letter Generator API",
    description="Backend API powered by Google Gemini 3.6 Flash",
    version="1.0.0"
)


class GenerationRequest(BaseModel):
    user_profile: str
    job_description: str
    document_type: Optional[str] = "all"  # "all", "resume", or "cover_letter"


class GenerationResponse(BaseModel):
    resume: Optional[str] = ""
    cover_letter: Optional[str] = ""


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
        resume_text = ""
        cover_letter_text = ""

        # Generate Resume if "all" or specifically "resume" is requested
        if request.document_type in ["resume", "all", None]:
            resume_text = generate_resume(
                user_profile=request.user_profile,
                job_description=request.job_description,
                temperature=0.2
            )

        # Generate Cover Letter if "all" or specifically "cover_letter" is requested
        if request.document_type in ["cover_letter", "all", None]:
            cover_letter_text = generate_cover_letter(
                user_profile=request.user_profile,
                job_description=request.job_description,
                temperature=0.7
            )

        return GenerationResponse(resume=resume_text, cover_letter=cover_letter_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))