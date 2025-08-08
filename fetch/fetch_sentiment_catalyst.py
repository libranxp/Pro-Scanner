# fetch/fetch_sentiment_catalyst.py
import requests
import os

LUNARCRUSH_KEY = os.environ["LUNARCRUSH_KEY"]

def get_sentiment_score(symbol):
    try:
        url = f"https://api.lunarcrush.com/v2?data=assets&key={LUNARCRUSH_KEY}&symbol={symbol}"
        res = requests.get(url).json()
        score = res["data"][0]["galaxy_score"]
        return score
    except:
        return 0
