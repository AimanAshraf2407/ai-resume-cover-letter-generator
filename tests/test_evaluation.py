import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from src.evaluation import extract_keywords, calculate_ats_metrics


def test_extract_keywords():
    sample = "FastAPI, Python 3.12, Docker, and PostgreSQL integration!"
    kws = extract_keywords(sample)
    assert "fastapi" in kws
    assert "python" in kws
    assert "and" not in kws  # Stopword removed


def test_calculate_ats_metrics():
    profile = "Python, FastAPI developer."
    job = "Looking for a Python and FastAPI developer."
    output = "Skilled Python and FastAPI developer."

    metrics = calculate_ats_metrics(profile, job, output)
    assert metrics["keyword_recall_pct"] > 0
    assert metrics["keyword_precision_pct"] > 0
    assert metrics["f1_score"] > 0