import os
import requests
from datetime import datetime

MESSARI_KEY = os.getenv("MESSARI_API_KEY")
LUNARCRUSH_KEY = os.getenv("LUNARCRUSH_KEY")
COINGLASS_KEY = os.getenv("COINGLASS_KEY")

def fetch_json(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=6)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}

def enrich_alert_data(raw):
    ticker = raw["ticker"]

    # Catalyst
    messari = fetch_json("https://data.messari.io/api/v1/news", {"filter": ticker})
    news = messari.get("data", [{}])[0]
    catalyst = news.get("title", "—")
    catalyst_link = news.get("url", "https://messari.io/news")

    # Sentiment
    lunar = fetch_json("https://api.lunarcrush.com/v2", {
        "data": "assets",
        "key": LUNARCRUSH_KEY,
        "symbol": ticker
    })
    asset = lunar.get("data", [{}])[0]
    sentiment_analysis = f"Galaxy Score: {asset.get('galaxy_score', '—')}"
    sentiment_surge = f"{asset.get('twitter_mentions_percent_change', '—')}% Twitter mentions"
    sentiment_link = f"https://lunarcrush.com/coins/{ticker.lower()}"

    # Order Book
    cg = fetch_json("https://open-api.coinglass.com/public/v2/open_interest", {
        "symbol": ticker
    }, headers={"coinglassSecret": COINGLASS_KEY})
    ob = cg.get("data", {})
    orderbook_wall = f"{ob.get('totalOpenInterest', '—')} OI"
    orderbook_exchange = ob.get("exchangeName", "—")

    return {
        **raw,
        "catalyst": catalyst,
        "catalyst_link": catalyst_link,
        "catalyst_link_text": "Messari",
        "sentiment_analysis": sentiment_analysis,
        "sentiment_surge": sentiment_surge,
        "sentiment_link": sentiment_link,
        "orderbook_wall": orderbook_wall,
        "orderbook_exchange": orderbook_exchange,
        "chart_link": f"https://www.tradingview.com/symbols/{ticker.replace('/', '')}",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    }
