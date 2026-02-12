import json
from collections import defaultdict

def load_tweets(path="tweets.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def categorize(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["java", "spring", "api", "python", "code", "backend"]):
        return "Software Developement"
    if any(k in t for k in ["ai", "robotics", "LLM", "chatGPT", "gemini", "grok", "AI model"]):
        return "Software Developement"
    if any(k in t for k in ["invest", "stock", "market", "sip", "nifty","AMD", "NVDA", "tesla", "crypto", "bitcoin", "ethereum"]):
        return "Finance"
    if any(k in t for k in ["discipline", "habit", "consistency", "mindset"]):
        return "Life Advice"
    if any(k in t for k in ["sleep", "focus", "routine", "productivity", "time", "energy", "job", "work"]):
        return "Productivity"
    return "Other"

def group_by_category(tweets):
    grouped = defaultdict(list)
    for tw in tweets:
        cat = categorize(tw["text"])
        grouped[cat].append(tw)
    return grouped

if __name__ == "__main__":
    tweets = load_tweets()
    grouped = group_by_category(tweets)
    for cat, items in grouped.items():
        print(cat, "=>", len(items))
