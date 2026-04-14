import pandas as pd
import matplotlib.pyplot as plt
import glob
import os



files = glob.glob("data/trends_*.csv")

if not files:
    print("No CSV files found. Run Task 2 first.")
    exit()

latest_file = max(files, key=os.path.getctime)
print(f"Loading file: {latest_file}")

df = pd.read_csv(latest_file)

category_counts = df["category"].value_counts()

plt.figure()
category_counts.plot(kind="bar")
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


avg_scores = df.groupby("category")["score"].mean()

plt.figure()
avg_scores.plot(kind="bar")
plt.title("Average Score per Category")
plt.xlabel("Category")
plt.ylabel("Average Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()