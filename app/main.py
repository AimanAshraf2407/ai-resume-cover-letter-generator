import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from models.generator import generate_resume, generate_cover_letter
from src.evaluation import calculate_ats_metrics

app = FastAPI(title="AI Resume & Cover Letter Generator API")

# Handles both HEAD and GET requests for health probes (satisfies Render health checks)
@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return {"status": "ok", "message": "Service is running"}


class GenerateRequest(BaseModel):
    user_profile: str
    job_description: str
    document_type: str = "both"  # Options: "resume", "cover_letter", "both"
    temperature: Optional[float] = 0.2


class GenerateResponse(BaseModel):
    resume: Optional[str] = None
    cover_letter: Optional[str] = None
    ats_score: Optional[float] = None
    evaluation_metrics: Optional[dict] = None


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_documents(payload: GenerateRequest):
    if not payload.user_profile.strip() or not payload.job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Profile and Job Description cannot be empty."
        )

    resume_text = None
    cover_letter_text = None

    try:
        if payload.document_type in ["resume", "both"]:
            resume_text = generate_resume(
                payload.user_profile,
                payload.job_description,
                temperature=payload.temperature,
            )

        if payload.document_type in ["cover_letter", "both"]:
            cover_letter_text = generate_cover_letter(
                payload.user_profile,
                payload.job_description,
                temperature=payload.temperature,
            )

        eval_text = resume_text if resume_text else cover_letter_text
        
        # Pass all 3 positional arguments: job_description, candidate_profile, generated_text
        metrics = {}
        if eval_text:
            try:
                metrics = calculate_ats_metrics(
                    payload.job_description,
                    payload.user_profile,
                    eval_text,
                )
            except TypeError:
                # Fallback in case parameter order in src/evaluation.py is (profile, job, text)
                metrics = calculate_ats_metrics(
                    payload.user_profile,
                    payload.job_description,
                    eval_text,
                )

        ats_score = metrics.get("recall") or metrics.get("ats_score") or metrics.get("ats_match_score")

        return GenerateResponse(
            resume=resume_text,
            cover_letter=cover_letter_text,
            ats_score=ats_score,
            evaluation_metrics=metrics,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))