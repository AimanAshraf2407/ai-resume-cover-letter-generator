import pandas as pd

# Load cleaned dataset
file = "data/processed/job_resume_fit_CLEAN.csv"
df = pd.read_csv(file)

print("===== DATASET OVERVIEW =====")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\n===== MISSING VALUES =====")
missing = df.isnull().sum()
print(missing)

print("\n===== MISSING PERCENTAGE =====")
missing_percentage = (df.isnull().sum() / len(df)) * 100
print(missing_percentage.round(2))

print("\n===== DUPLICATE ROWS =====")
print("Duplicate rows:", df.duplicated().sum())

print("\n===== CATEGORIES =====")
print("Number of unique categories:", df["category"].nunique())
print("\nTop categories:")
print(df["category"].value_counts().head(20))

print("\n===== SCORE INFORMATION =====")

score_columns = [
    "ai_match_score",
    "skill_string_match_score",
    "fuzzy_match_score"
]

for column in score_columns:
    # Convert values to numbers
    # Invalid text values become missing (NaN)
    df[column] = pd.to_numeric(df[column], errors="coerce")

    print(f"\n{column}")
    print("Minimum:", df[column].min())
    print("Maximum:", df[column].max())
    print("Average:", round(df[column].mean(), 2))
    print("Missing:", df[column].isnull().sum())

print("\n===== SAMPLE RESUME =====")
print(df["resume_text"].iloc[0])

print("\n===== SAMPLE JOB DESCRIPTION =====")
print(df["job_text"].iloc[0])

print("\n===== SAMPLE REQUIRED SKILLS =====")
print(df["job_required_skills"].iloc[0])

print("\n===== SAMPLE RESUME SKILLS =====")
print(df["resume_skill_list"].iloc[0])