import pandas as pd
import glob
import os

print("Task 3 started...")

# Step 1: Load latest CSV file
files = glob.glob("data/trends_*.csv")

if not files:
    print("No CSV files found. Run Task 2 first.")
    exit()

latest_file = max(files, key=os.path.getctime)
print(f"Loading file: {latest_file}")

df = pd.read_csv(latest_file)

# Step 2: Basic info
print("\nTotal Stories Collected:", len(df))

# Step 3: Stories per category
print("\nStories per Category:")
category_counts = df["category"].value_counts()
print(category_counts)

# Step 4: Average score per category
print("\nAverage Score per Category:")
avg_scores = df.groupby("category")["score"].mean()
print(avg_scores)

# Step 5: Top 5 highest scored stories
print("\nTop 5 Highest Scored Stories:")
top_stories = df.sort_values(by="score", ascending=False)[["title", "score", "category"]].head(5)
print(top_stories)