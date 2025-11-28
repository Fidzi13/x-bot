# Render Bot Package (Siap Deploy)

## main.py

```python
import os
import time
import random
import requests
import json

AUTH = os.getenv("AUTH_TOKEN")
CT0 = os.getenv("CT0")
BEARER = os.getenv("BEARER")
TARGET_ACCOUNTS = os.getenv("ACCOUNTS", "").split(",")
CTA_LINKS = os.getenv("CTA_LINKS", "").split(";")
MODE = os.getenv("MODE", "C")

HEADERS = {
    "authorization": f"Bearer {BEARER}",
    "cookie": f"auth_token={AUTH}; ct0={CT0}",
    "x-csrf-token": CT0,
    "content-type": "application/json"
}


def get_tweets(user):
    url = f"https://api.twitter.com/2/timeline/profile/{user}.json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.json()
    except:
        return None


def extract_tweet_ids(data):
    ids = []
    try:
        for entry in data.get("globalObjects", {}).get("tweets", {}).values():
            if int(entry.get("retweet_count", 0)) > 500 or int(entry.get("favorite_count", 0)) > 1000:
                ids.append(entry.get("id_str"))
        return ids
    except:
        return []


def comment(tweet_id, text):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    payload = {
        "status": text,
        "in_reply_to_status_id": tweet_id,
        "auto_populate_reply_metadata": True
    }
    r = requests.post(url, headers=HEADERS, json=payload)
    return r.status_code, r.text


def random_comment():
    CTA = random.choice(CTA_LINKS)
    comments = [
        f"This is really interesting! Check this out too: {CTA}",
        f"Great post! You might want to see this as well: {CTA}",
        f"Love this! Sharing something useful here: {CTA}",
    ]
    return random.choice(comments)


if __name__ == "__main__":
    print("Bot started...")
    while True:
        for account in TARGET_ACCOUNTS:
            print(f"Scanning: {account}")
            data = get_tweets(account)
            if not data:
                continue

            tweet_ids = extract_tweet_ids(data)
            for tid in tweet_ids:
                print(f"Commenting on tweet: {tid}")
                text = random_comment()
                status, res = comment(tid, text)
                print(status, res)
                time.sleep(random.randint(5, 12))

        sleep_time = random.randint(300, 600)  # 5–10 menit
        print(f"Sleeping {sleep_time} sec...\n")
        time.sleep(sleep_time)
```

---

## requirements.txt

```
requests
python-dotenv
```

---

## Procfile

```
worker: python main.py
```

---

## .env example

```
AUTH_TOKEN=isi_disini
CT0=isi_disini
BEARER=AAAAAAAAAAAAAAAAAAAAANRILgAAAAA...
ACCOUNTS=elonmusk,binance,solana,layerzero_labs
CTA_LINKS=https://short.id/a1;https://short.id/a2;https://short.id/a3
MODE=C
```
