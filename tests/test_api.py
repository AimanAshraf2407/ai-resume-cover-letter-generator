import sys
from pathlib import Path
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

# Ensure root directory is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from app.main import app


@pytest.fixture
def client():
    """Provides a fresh TestClient instance for tests."""
    with TestClient(app) as test_client:
        yield test_client


def test_root_endpoint(client):
    """Verify that the root endpoint is alive and returns status 200."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data or "status" in data


@patch("app.main.generate_resume")
@patch("app.main.generate_cover_letter")
def test_generate_endpoint_success(mock_cover, mock_resume, client):
    """Verify that POST /api/generate returns tailored resume and cover letter."""
    # Mock LLM outputs to isolate testing and avoid external rate limits
    mock_resume.return_value = (
        "# ALEX CHEN\n\n## PROFESSIONAL SUMMARY\n"
        "Experienced Backend Engineer skilled in Python, FastAPI, and Docker microservices."
    )
    mock_cover.return_value = (
        "Dear Hiring Team,\n\nI am writing to express my strong interest in the "
        "Junior Software Engineer role. I bring relevant experience in Python and FastAPI."
    )

    payload = {
        "user_profile": "Alex Chen. Skills: Python, FastAPI. Experience: 1 year backend intern.",
        "job_description": "Junior Software Engineer requiring Python and FastAPI backend development.",
        "document_type": "all"
    }

    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "resume" in data
    assert "cover_letter" in data
    assert len(data["resume"]) > 50
    assert len(data["cover_letter"]) > 50

    # Ensure mock functions were invoked
    mock_resume.assert_called_once()
    mock_cover.assert_called_once()


def test_generate_endpoint_missing_fields(client):
    """Verify that sending missing fields fails validation with 422 Unprocessable Entity."""
    invalid_payload = {
        "user_profile": "Alex Chen"
        # 'job_description' intentionally missing
    }

    response = client.post("/api/generate", json=invalid_payload)
    assert response.status_code == 422