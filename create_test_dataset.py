import pandas as pd

# Load cleaned dataset
input_file = "data/processed/job_resume_fit_CLEAN.csv"
df = pd.read_csv(input_file)

# Make sure score columns are numeric
score_columns = [
    "ai_match_score",
    "skill_string_match_score",
    "fuzzy_match_score"
]

for column in score_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")


# ==========================================
# SELECT TEST CASES
# ==========================================

test_cases = []

# T01 - High match
row = df.loc[df["ai_match_score"].idxmax()]
test_cases.append(("T01", "Strong resume - matching job", row))

# T02 - Low match
row = df.loc[df["ai_match_score"].idxmin()]
test_cases.append(("T02", "Weak resume - low matching job", row))

# T03 - High skill string match
row = df.loc[df["skill_string_match_score"].idxmax()]
test_cases.append(("T03", "High skill match", row))

# T04 - Low skill string match
row = df.loc[df["skill_string_match_score"].idxmin()]
test_cases.append(("T04", "Low skill match", row))

# T05 - High fuzzy match
row = df.loc[df["fuzzy_match_score"].idxmax()]
test_cases.append(("T05", "High fuzzy matching", row))

# T06 - Low fuzzy match
row = df.loc[df["fuzzy_match_score"].idxmin()]
test_cases.append(("T06", "Low fuzzy matching", row))


# ==========================================
# CATEGORY TESTS
# ==========================================

categories = [
    "HR",
    "INFORMATION-TECHNOLOGY",
    "FINANCE",
    "ENGINEERING"
]

test_number = 7

for category in categories:

    category_data = df[
        df["category"].astype(str).str.upper() == category
    ]

    if len(category_data) > 0:

        # Select the first available record
        row = category_data.iloc[0]

        test_cases.append(
            (
                f"T{test_number:02d}",
                f"{category} category test",
                row
            )
        )

        test_number += 1


# ==========================================
# RANDOM TEST CASES
# ==========================================

remaining = df.sample(
    n=20,
    random_state=42
)

for _, row in remaining.iterrows():

    if len(test_cases) >= 20:
        break

    test_cases.append(
        (
            f"T{len(test_cases)+1:02d}",
            "General random test",
            row
        )
    )


# ==========================================
# CREATE TEST DATAFRAME
# ==========================================

records = []

for test_id, scenario, row in test_cases:

    records.append({
        "test_id": test_id,
        "scenario": scenario,
        "source_id": row["ID"],
        "category": row["category"],
        "resume_text": row["resume_text"],
        "job_text": row["job_text"],
        "job_required_skills": row["job_required_skills"],
        "resume_skill_list": row["resume_skill_list"],
        "baseline_ai_match_score": row["ai_match_score"],
        "baseline_skill_match_score": row["skill_string_match_score"],
        "baseline_fuzzy_match_score": row["fuzzy_match_score"]
    })


test_df = pd.DataFrame(records)

# Remove duplicate source records
test_df = test_df.drop_duplicates(subset=["source_id"])

# Save test dataset
output_file = "tests/test_dataset.csv"

test_df.to_csv(output_file, index=False)

print("===== TEST DATASET CREATED =====")
print("Number of test cases:", len(test_df))
print("\nTest cases:")
print(test_df[["test_id", "scenario", "source_id", "category"]].to_string(index=False))

print("\nSaved to:")
print(output_file)