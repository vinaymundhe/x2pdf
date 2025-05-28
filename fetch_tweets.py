import os
import requests
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

def create_headers():
    return {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = create_headers()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']['id']

def get_tweets(user_id, max_results=10):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    headers = create_headers()
    params = {
        "max_results": max_results,
        "tweet.fields": "created_at,text"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['data']

if __name__ == "__main__":
    username = "vinaymundhe_"  # <--- CHANGE THIS to your X handle, no '@'
    user_id = get_user_id(username)
    tweets = get_tweets(user_id)
    for tweet in tweets:
        print(f"{tweet['created_at']}: {tweet['text']}\n")
