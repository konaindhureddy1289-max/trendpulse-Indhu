import pandas as pd
import glob
import os

print("Task 2 started...")

files = glob.glob("data/trends_*.json")
print("Files found:", files)

if not files:
    print("No JSON files found in data/ folder")
    exit()

latest_file = max(files, key=os.path.getctime)
print(f"Loading file: {latest_file}")

df = pd.read_json(latest_file)

print("Original Data Shape:", df.shape)

df.dropna(inplace=True)
df.drop_duplicates(subset="post_id", inplace=True)

df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

df.dropna(subset=["score", "num_comments"], inplace=True)

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

print("Cleaned Data Shape:", df.shape)

csv_file = latest_file.replace(".json", ".csv")
df.to_csv(csv_file, index=False)

print(f" Cleaned CSV saved to: {csv_file}")