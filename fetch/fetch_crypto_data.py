import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

BST = ZoneInfo("Europe/London")

CMC_KEY = os.getenv("CMC_KEY")
LUNARCRUSH_KEY = os.getenv("LUNARCRUSH_KEY")
MESSARI_KEY = os.getenv("MESSARI_KEY")

def fetch_cmc_data(symbol):
    """
    Pull price, volume, percent change via CoinMarketCap.
    """
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}"
    headers = {"X-CMC_PRO_API_KEY": CMC_KEY}

    try:
        res = requests.get(url, headers=headers)
        data = res.json()["data"][symbol]

        return {
            "price": round(data["quote"]["USD"]["price"], 6),
            "volume_24h": data["quote"]["USD"]["volume_24h"],
            "percent_change": data["quote"]["USD"]["percent_change_24h"]
        }
    except Exception as e:
        print(f"[CMC] Error fetching {symbol}: {e}")
        return {}

def fetch_lunarcrush_data(symbol):
    """
    Get sentiment and Galaxy Score from LunarCrush.
    """
    url = f"https://api.lunarcrush.com/v2?data=assets&key={LUNARCRUSH_KEY}&symbol={symbol}"

    try:
        res = requests.get(url)
        raw = res.json().get("data", [{}])[0]
        return {
            "galaxy_score": raw.get("galaxy_score"),
            "alt_rank": raw.get("alt_rank"),
            "twitter_mentions": raw.get("twitter_mentions"),
            "social_score": raw.get("social_score"),
            "sentiment": raw.get("average_sentiment", 0)
        }
    except Exception as e:
        print(f"[LunarCrush] Error fetching {symbol}: {e}")
        return {}

def fetch_messari_data(symbol):
    """
    Get supply and market cap via Messari.
    """
    url = f"https://data.messari.io/api/v1/assets/{symbol.lower()}/metrics"
    headers = {"x-messari-api-key": MESSARI_KEY}

    try:
        res = requests.get(url, headers=headers)
        metrics = res.json()["data"]

        return {
            "market_cap": metrics["marketcap"]["current_marketcap_usd"],
            "circulating_supply": metrics["supply"]["circulating"],
            "liquid_supply": metrics["supply"]["liquid"]
        }
    except Exception as e:
        print(f"[Messari] Error fetching {symbol}: {e}")
        return {}

def fetch_crypto_data(symbol):
    """
    Unified crypto data fetch across all sources.
    """
    cmc = fetch_cmc_data(symbol)
    sentiment = fetch_lunarcrush_data(symbol)
    fundamentals = fetch_messari_data(symbol)

    return {
        "symbol": symbol,
        "asset_type": "crypto",
        "price": cmc.get("price", 0),
        "percent_change": cmc.get("percent_change", 0),
        "volume_24h": cmc.get("volume_24h", 0),
        "galaxy_score": sentiment.get("galaxy_score", 0),
        "alt_rank": sentiment.get("alt_rank", 0),
        "twitter_mentions": sentiment.get("twitter_mentions", 0),
        "social_score": sentiment.get("social_score", 0),
        "average_sentiment": sentiment.get("sentiment", 0),
        "market_cap": fundamentals.get("market_cap", 0),
        "circulating_supply": fundamentals.get("circulating_supply", 0),
        "liquid_supply": fundamentals.get("liquid_supply", 0),
        "timestamp": datetime.now(tz=BST).strftime("%Y-%m-%d %H:%M:%S %Z")
    }
