import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

# Allow imports from project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation import calculate_ats_metrics


# =========================
# Project configuration
# =========================

TEST_DATASET = PROJECT_ROOT / "tests" / "test_dataset.csv"

OUTPUT_DIR = PROJECT_ROOT / "results" / "generated_outputs"

RESULTS_FILE = PROJECT_ROOT / "results" / "p3_automated_results.csv"

JSON_RESULTS_FILE = PROJECT_ROOT / "results" / "p3_automated_results.json"

API_URL = "http://127.0.0.1:8000/api/generate"


# =========================
# API request
# =========================

def generate_with_api(user_profile: str, job_description: str) -> dict:
    """
    Send one request to the group's API.

    The API generates both:
    - Resume
    - Cover letter
    """

    payload = {
        "user_profile": user_profile,
        "job_description": job_description,
    }

    data = json.dumps(payload).encode("utf-8")

    request = Request(
        API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=180) as response:
            response_data = response.read().decode("utf-8")

        result = json.loads(response_data)

        return {
            "resume": result.get("resume", ""),
            "cover_letter": result.get("cover_letter", ""),
        }

    except HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"API request failed with HTTP {error.code}: {error_body}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            "Could not connect to the AI API. "
            "Make sure the FastAPI server is running."
        ) from error


# =========================
# Evaluation
# =========================

def run_evaluation(max_cases: int = 20, delay_seconds: int = 10):
    """Run automated evaluation using the group's API."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not TEST_DATASET.exists():
        raise FileNotFoundError(
            f"Test dataset not found: {TEST_DATASET}"
        )

    df = pd.read_csv(TEST_DATASET).head(max_cases)

    results = []

    print("=" * 70)
    print("PERSON 3 - AUTOMATED AI EVALUATION")
    print("=" * 70)
    print(f"Test cases: {len(df)}")
    print(f"API endpoint: {API_URL}")
    print()

    for index, row in df.iterrows():

        test_id = str(row["test_id"])

        print(
            f"[{index + 1}/{len(df)}] Evaluating {test_id}..."
        )

        user_profile = str(row["resume_text"])
        job_description = str(row["job_text"])

        start_time = time.time()

        # IMPORTANT:
        # One API request generates BOTH outputs.
        generated = generate_with_api(
            user_profile,
            job_description
        )

        latency = round(time.time() - start_time, 2)

        resume_text = generated["resume"]
        cover_letter_text = generated["cover_letter"]

        # Save raw outputs immediately
        resume_file = OUTPUT_DIR / f"{test_id}_resume.md"

        cover_letter_file = (
            OUTPUT_DIR / f"{test_id}_cover_letter.md"
        )

        resume_file.write_text(
            resume_text,
            encoding="utf-8"
        )

        cover_letter_file.write_text(
            cover_letter_text,
            encoding="utf-8"
        )

        # =========================
        # Resume ATS metrics
        # =========================

        resume_metrics = calculate_ats_metrics(
            user_profile,
            job_description,
            resume_text
        )

        # =========================
        # Cover letter ATS metrics
        # =========================

        cover_letter_metrics = calculate_ats_metrics(
            user_profile,
            job_description,
            cover_letter_text
        )

        # =========================
        # Store results
        # =========================

        result = {
            "test_id": test_id,
            "scenario": row["scenario"],
            "category": row["category"],

            "resume_recall_pct": (
                resume_metrics["keyword_recall_pct"]
            ),

            "resume_precision_pct": (
                resume_metrics["keyword_precision_pct"]
            ),

            "resume_f1": (
                resume_metrics["f1_score"]
            ),

            "resume_word_count": len(
                resume_text.split()
            ),

            "cover_letter_recall_pct": (
                cover_letter_metrics["keyword_recall_pct"]
            ),

            "cover_letter_precision_pct": (
                cover_letter_metrics["keyword_precision_pct"]
            ),

            "cover_letter_f1": (
                cover_letter_metrics["f1_score"]
            ),

            "cover_letter_word_count": len(
                cover_letter_text.split()
            ),

            "latency_seconds": latency,

            "resume_output_file": str(resume_file),

            "cover_letter_output_file": (
                str(cover_letter_file)
            ),
        }

        results.append(result)

        print(
            f"  Resume F1: "
            f"{result['resume_f1']:.2f}%"
        )

        print(
            f"  Cover Letter F1: "
            f"{result['cover_letter_f1']:.2f}%"
        )

        print(
            f"  Latency: "
            f"{latency}s"
        )

        # Delay to reduce rate-limit pressure
        if (
            delay_seconds > 0
            and index < len(df) - 1
        ):
            print(
                f"  Waiting {delay_seconds}s..."
            )
            time.sleep(delay_seconds)

    # =========================
    # Save CSV results
    # =========================

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        RESULTS_FILE,
        index=False
    )

    # =========================
    # Save JSON results
    # =========================

    JSON_RESULTS_FILE.write_text(
        json.dumps(
            results,
            indent=2
        ),
        encoding="utf-8"
    )

    # =========================
    # Final summary
    # =========================

    print()
    print("=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)

    print(
        f"CSV results: {RESULTS_FILE}"
    )

    print(
        f"JSON results: {JSON_RESULTS_FILE}"
    )

    print(
        f"Generated outputs: {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    run_evaluation()