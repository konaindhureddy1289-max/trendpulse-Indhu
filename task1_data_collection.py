import requests
import time
import json
import os
from datetime import datetime

# API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

# Categories and keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm", "programming", "developer"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global", "policy"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship", "match"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome", "experiment"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming", "series"]
}

# Function to assign category (with fallback)
def get_category(title, category_counts):
    title = title.lower()

    # Try keyword match first
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title:
                return category

    # Fallback: assign to category with least count
    remaining = [cat for cat in categories if category_counts[cat] < 25]

    if remaining:
        return min(remaining, key=lambda x: category_counts[x])

    return None

# Fetch data
def fetch_data():
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        story_ids = response.json() [:500]
    except Exception as e:
        print("Error fetching top stories:", e)
        return []

    collected = []
    category_counts = {cat: 0 for cat in categories}

    for story_id in story_ids:
        try:
            res = requests.get(ITEM_URL.format(story_id), headers=headers)
            story = res.json()
        except Exception as e:
            print(f"Failed to fetch story {story_id}: {e}")
            continue

        # Skip invalid stories
        if not story or "title" not in story:
            continue

        # Get category (with fallback logic)
        category = get_category(story["title"], category_counts)

        # Add story if category not full
        if category and category_counts[category] < 25:
            data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected.append(data)
            category_counts[category] += 1

            print(f"{category}: {category_counts[category]} collected")

            # Sleep only when category is completed
            if category_counts[category] == 25:
                print(f"Collected 25 stories for {category}, waiting 2 seconds...")
                time.sleep(2)

        # Stop when all categories reach 25
        if all(count >= 25 for count in category_counts.values()):
            break

    return collected

# Save JSON
def save_json(data):
    os.makedirs("data", exist_ok=True)

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print("\nFinal Category Counts:")
    for cat in categories:
        print(f"{cat}: {sum(1 for d in data if d['category'] == cat)}")

    print(f"\nCollected {len(data)} stories.")
    print(f"Saved to {filename}")

# Run program
if __name__ == "__main__":
    data = fetch_data()
    save_json(data)