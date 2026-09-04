import pandas as pd

# Load the original dataset
input_file = "data/raw/job_resume_fit.csv"

df = pd.read_csv(input_file)

print("===== BEFORE CLEANING =====")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Remove completely empty columns
df = df.dropna(axis=1, how="all")

# Remove unwanted Unnamed columns
df = df.loc[:, ~df.columns.str.startswith("Unnamed:")]

print("\n===== AFTER REMOVING UNWANTED COLUMNS =====")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Columns that are important for our project
important_columns = [
    "ID",
    "resume_text",
    "job_text",
    "category",
    "job_required_skills",
    "resume_skill_list",
    "ai_matched_skills",
    "ai_match_score",
    "skill_string_match_score",
    "fuzzy_match_score"
]

# Keep only important columns that actually exist
available_columns = [
    column for column in important_columns
    if column in df.columns
]

df_clean = df[available_columns].copy()

# Remove rows where resume or job description is missing
df_clean = df_clean.dropna(
    subset=["resume_text", "job_text"]
)

# Remove duplicate rows
df_clean = df_clean.drop_duplicates()

# Save the cleaned dataset
output_file = "data/processed/job_resume_fit_CLEAN.csv"

df_clean.to_csv(output_file, index=False)

print("\n===== CLEANING COMPLETE =====")
print("Final rows:", len(df_clean))
print("Final columns:", len(df_clean.columns))

print("\n===== FINAL COLUMNS =====")
for column in df_clean.columns:
    print(column)

print("\nClean dataset saved to:")
print(output_file)