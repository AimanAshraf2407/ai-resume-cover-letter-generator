import json
import time
from pathlib import Path
from models.generator import generate_resume
from src.evaluation import calculate_ats_metrics

def run_batch_evaluation():
    print("🚀 Running Automated ATS Evaluation Pipeline...\n")

    base_dir = Path(__file__).resolve().parent
    profile_path = base_dir / "data" / "sample_profiles" / "profile_01_software_engineer.json"
    job_path = base_dir / "data" / "sample_job_descriptions" / "job_01_junior_ai_engineer.txt"

    with open(profile_path, "r", encoding="utf-8") as f:
        profile_data = json.load(f)
    user_profile = json.dumps(profile_data, indent=2)

    with open(job_path, "r", encoding="utf-8") as f:
        job_description = f.read()

    temperatures = [0.2, 0.7]
    evaluation_records = []

    for temp in temperatures:
        print(f"🔄 Evaluating Generation @ Temperature = {temp}...")
        start_time = time.time()
        resume_md = generate_resume(user_profile, job_description, temperature=temp)
        latency = round(time.time() - start_time, 2)

        metrics = calculate_ats_metrics(user_profile, job_description, resume_md)
        metrics["temperature"] = temp
        metrics["latency_seconds"] = latency
        metrics["word_count"] = len(resume_md.split())
        evaluation_records.append(metrics)
        
        print("⏳ Spacing requests (10s delay to protect free tier quota)...")
        time.sleep(10)

    print("\n" + "=" * 80)
    print("📊 BIT 4543 MODEL EVALUATION RESULTS (CHAPTER 5.3)")
    print("=" * 80)
    
    header = f"{'Temp':<6} | {'Recall (ATS %)':<16} | {'Precision %':<14} | {'F1-Score':<10} | {'Latency (s)':<12} | {'Words':<6}"
    print(header)
    print("-" * len(header))
    
    for r in evaluation_records:
        row = (
            f"{r['temperature']:<6} | "
            f"{r['keyword_recall_pct']:<16} | "
            f"{r['keyword_precision_pct']:<14} | "
            f"{r['f1_score']:<10} | "
            f"{r['latency_seconds']:<12} | "
            f"{r['word_count']:<6}"
        )
        print(row)
    print("=" * 80)

if __name__ == "__main__":
    run_batch_evaluation()