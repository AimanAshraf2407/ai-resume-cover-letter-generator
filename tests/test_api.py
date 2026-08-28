import sys
import time
from pathlib import Path
from fastapi.testclient import TestClient

# Add project root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Verify that the root endpoint is alive and returns status 200."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data or "status" in data


def test_generate_endpoint_success():
    """Verify that POST /api/generate returns tailored resume and cover letter."""
    payload = {
        "user_profile": "Alex Chen. Skills: Python, FastAPI. Experience: 1 year backend intern.",
        "job_description": "Junior Software Engineer requiring Python and FastAPI backend development."
    }
    
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "resume" in data
    assert "cover_letter" in data
    assert len(data["resume"]) > 50
    assert len(data["cover_letter"]) > 50


def test_generate_endpoint_missing_fields():
    """Verify that sending empty/missing fields returns 422 Unprocessable Entity."""
    time.sleep(1.0)  # Brief pause to avoid API rate bursts
    
    # Missing 'job_description'
    invalid_payload = {
        "user_profile": "Alex Chen"
    }
    
    response = client.post("/api/generate", json=invalid_payload)
    assert response.status_code == 422