import requests
import time
import os
import tweepy

# Twitter API 凭证
CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Server酱配置
SCKEY = os.getenv("SERVER_CHAN_KEY")
SERVERCHAN_URL = f"https://sctapi.ftqq.com/{SCKEY}.send"

# 要监控的用户
TWITTER_USERNAME = "binancezh"

def get_latest_tweet(client, username):
    user = client.get_user(username=username).data
    tweets = client.get_users_tweets(id=user.id, max_results=5)
    return tweets.data[0].text if tweets.data else None

def send_to_wechat(text):
    requests.post(SERVERCHAN_URL, data={
        "title": "Twitter新动态",
        "desp": text
    })

def main():
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    latest = get_latest_tweet(client, TWITTER_USERNAME)
    cache_file = "latest.txt"
    
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            last = f.read().strip()
    else:
        last = ""

    if latest and latest != last:
        send_to_wechat(latest)
        with open(cache_file, "w") as f:
            f.write(latest)
        print("新推文已发送")
    else:
        print("无新推文")

if __name__ == "__main__":
    main()
