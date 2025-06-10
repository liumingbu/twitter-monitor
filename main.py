import snscrape.modules.twitter as sntwitter
import requests
import os
import json

USERNAME = "binancezh"
SENDKEY = os.environ.get("SENDKEY", "")
STATE_FILE = "last_tweet.json"

def get_latest_tweet():
    for tweet in sntwitter.TwitterUserScraper(USERNAME).get_items():
        return {"id": tweet.id, "content": tweet.content}

def load_last_tweet_id():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f).get("id")
    return None

def save_latest_tweet(tweet):
    with open(STATE_FILE, "w") as f:
        json.dump(tweet, f)

def send_serverchan(content):
    if not SENDKEY:
        print("No Server酱 SendKey set")
        return
    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"
    data = {
        "title": "📢 @binancezh 有新推文",
        "desp": content
    }
    requests.post(url, data=data)

def main():
    latest_tweet = get_latest_tweet()
    last_id = load_last_tweet_id()
    if str(latest_tweet["id"]) != str(last_id):
        print("New tweet detected")
        send_serverchan(latest_tweet['content'])
        save_latest_tweet(latest_tweet)
    else:
        print("No new tweet")

if __name__ == "__main__":
    main()
