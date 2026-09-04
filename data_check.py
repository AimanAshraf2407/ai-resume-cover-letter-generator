import pandas as pd

# Load the dataset
df = pd.read_csv("data/raw/job_resume_fit.csv")

# Basic information
print("===== DATASET INFORMATION =====")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Show all column names
print("\n===== COLUMN NAMES =====")
for column in df.columns:
    print(column)

# Check missing values
print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

# Show first 5 rows
print("\n===== FIRST 5 ROWS =====")
print(df.head())