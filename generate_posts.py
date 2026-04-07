from openai import OpenAI

def generate_similar_tweets(tweets, count=5):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Extract writing style from existing tweets
    sample = "\n".join([t["text"] for t in tweets[:10]])
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{
            "role": "user",
            "content": f"""Analyze the writing style and topics in these tweets, then generate {count} NEW original tweets in the same style:

{sample}

Generate {count} tweets that match this person's style, topics, and tone. Output one tweet per line."""
        }]
    )
    
    return response.choices[0].message.content.strip().split("\n")