import sys
import time
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from models.generator import generate_resume, generate_cover_letter


def test_resume_generation():
    sample_profile = "Alex Chen. Skills: Python, FastAPI. Experience: Built backend APIs."
    sample_job = "Looking for a Python Developer proficient in FastAPI."
    
    output = generate_resume(sample_profile, sample_job, temperature=0.2)
    
    assert isinstance(output, str)
    assert len(output) > 100
    assert "Alex Chen" in output or "FastAPI" in output


def test_cover_letter_generation():
    # Pause briefly to prevent rate spike
    time.sleep(1.5)
    
    sample_profile = "Alex Chen. Skills: Python, FastAPI."
    sample_job = "Looking for a Python Developer proficient in FastAPI."
    
    output = generate_cover_letter(sample_profile, sample_job, temperature=0.5)
    
    assert isinstance(output, str)
    assert len(output) > 100