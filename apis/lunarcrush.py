# apis/lunarcrush.py
import requests, os

def get_sentiment(symbol):
    url = f"https://api.lunarcrush.com/v2?data=assets&key={os.environ['LUNARCRUSH_KEY']}&symbol={symbol}"
    res = requests.get(url).json()
    return res["data"][0]["galaxy_score"]
