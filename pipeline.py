from fetch_tweets import get_user_id, get_tweets
from export_pdf import group, export_pdf

username = "vinaymundhe_"   # change here once

# 1. Fetch
user_id = get_user_id(username)
tweets = get_tweets(user_id)

# 2. Group
grouped = group(tweets)

# 3. Export
export_pdf(grouped, username)

print("Pipeline completed successfully.")