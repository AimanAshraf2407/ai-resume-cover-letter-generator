import sys
import json
import time
from pathlib import Path

import pandas as pd

# Allow this script to import modules from the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from models.generator import generate_resume, generate_cover_letter
from src.evaluation import calculate_ats_metrics


# Project paths
TEST_DATASET = PROJECT_ROOT / "tests" / "test_dataset.csv"
OUTPUT_DIR = PROJECT_ROOT / "results" / "generated_outputs"
RESULTS_FILE = PROJECT_ROOT / "results" / "p3_automated_results.csv"


def run_evaluation(max_cases: int = 20, delay_seconds: int = 10):
    """Run automated evaluation on the selected test cases."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not TEST_DATASET.exists():
        raise FileNotFoundError(f"Test dataset not found: {TEST_DATASET}")

    df = pd.read_csv(TEST_DATASET)

    # Limit the number of test cases if requested
    df = df.head(max_cases)

    results = []

    print("=" * 70)
    print("PERSON 3 - AUTOMATED AI EVALUATION")
    print("=" * 70)
    print(f"Test cases: {len(df)}")
    print()

    for _, row in df.iterrows():
        test_id = str(row["test_id"])

        print(f"Evaluating {test_id}...")

        user_profile = str(row["resume_text"])
        job_description = str(row["job_text"])

        start_time = time.time()

        # Generate resume
        resume_text = generate_resume(
            user_profile,
            job_description,
            temperature=0.2
        )

        # Generate cover letter
        cover_letter_text = generate_cover_letter(
            user_profile,
            job_description,
            temperature=0.5
        )

        latency = round(time.time() - start_time, 2)

        # Save raw AI outputs immediately
        resume_file = OUTPUT_DIR / f"{test_id}_resume.md"
        cover_letter_file = OUTPUT_DIR / f"{test_id}_cover_letter.md"

        resume_file.write_text(resume_text or "", encoding="utf-8")
        cover_letter_file.write_text(
            cover_letter_text or "",
            encoding="utf-8"
        )

        # Automated ATS evaluation for resume
        resume_metrics = calculate_ats_metrics(
            user_profile,
            job_description,
            resume_text or ""
        )

        # Automated ATS evaluation for cover letter
        cover_letter_metrics = calculate_ats_metrics(
            user_profile,
            job_description,
            cover_letter_text or ""
        )

        result = {
            "test_id": test_id,
            "scenario": row["scenario"],
            "category": row["category"],
            "resume_recall_pct": resume_metrics["keyword_recall_pct"],
            "resume_precision_pct": resume_metrics["keyword_precision_pct"],
            "resume_f1": resume_metrics["f1_score"],
            "resume_word_count": len((resume_text or "").split()),
            "cover_letter_recall_pct": cover_letter_metrics[
                "keyword_recall_pct"
            ],
            "cover_letter_precision_pct": cover_letter_metrics[
                "keyword_precision_pct"
            ],
            "cover_letter_f1": cover_letter_metrics["f1_score"],
            "cover_letter_word_count": len(
                (cover_letter_text or "").split()
            ),
            "latency_seconds": latency,
            "resume_output_file": str(resume_file),
            "cover_letter_output_file": str(cover_letter_file),
        }

        results.append(result)

        print(
            f"  Resume F1: {result['resume_f1']} | "
            f"Cover Letter F1: {result['cover_letter_f1']} | "
            f"Latency: {latency}s"
        )

        # Delay between test cases to reduce quota/rate-limit pressure
        if delay_seconds > 0:
            print(f"  Waiting {delay_seconds}s...")
            time.sleep(delay_seconds)

    # Save automated results
    results_df = pd.DataFrame(results)
    results_df.to_csv(RESULTS_FILE, index=False)

    # Save JSON copy for easier inspection
    json_file = PROJECT_ROOT / "results" / "p3_automated_results.json"
    json_file.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8"
    )

    print()
    print("=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)
    print(f"CSV results: {RESULTS_FILE}")
    print(f"JSON results: {json_file}")
    print(f"Generated outputs: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_evaluation()