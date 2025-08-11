import os
import requests

# Load secrets from environment
FMP_KEY = os.getenv("FMP_KEY")
FINNHUB_KEY = os.getenv("FINNHUB_KEY")
CMC_KEY = os.getenv("CMC_KEY")
MESSARI_KEY = os.getenv("MESSARI_API_KEY")
LUNARCRUSH_KEY = os.getenv("LUNARCRUSH_KEY")
COINGLASS_KEY = os.getenv("COINGLASS_KEY")
SANTIMENT_KEY = os.getenv("SANTIMENT_API_KEY")

def fetch_json(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=6)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}

# 🔹 STOCK DATA
def get_fmp_data(ticker_or_type):
    if ticker_or_type == "screener":
        return [s["symbol"] for s in fetch_json(
            "https://financialmodelingprep.com/api/v3/stock-screener",
            {"marketCapMoreThan": 1_000_000_000, "volumeMoreThan": 500_000, "limit": 50, "apikey": FMP_KEY}
        )]
    else:
        data = fetch_json(f"https://financialmodelingprep.com/api/v3/quote/{ticker_or_type}", {"apikey": FMP_KEY})
        if not data or not isinstance(data, list):
            return {}
        d = data[0]
        return {
            "price": d.get("price", 0),
            "previousClose": d.get("previousClose", 0),
            "dayLow": d.get("dayLow", 0),
            "dayHigh": d.get("dayHigh", 0),
            "yearHigh": d.get("yearHigh", 0),
            "volume": d.get("volume", 0),
            "exchange": d.get("exchange", "Unknown"),
            "premarket_gap": d.get("changesPercentage", 0),
            "rvol": d.get("rvol", 1),
            "float": d.get("float", 100_000_000),
            "short_interest": d.get("shortPercentFloat", 0),
            "atr_spike": d.get("atrSpike", 1),
            "resistance_gap": d.get("resistanceGap", 10)
        }

# 🔹 CRYPTO DATA
def get_crypto_data(ticker_or_type):
    if ticker_or_type == "list":
        data = fetch_json("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest", {
            "limit": 50
        }, headers={"X-CMC_PRO_API_KEY": CMC_KEY})
        return [coin["symbol"] + "USD" for coin in data.get("data", [])]
    else:
        # Simulated crypto data structure
        return {
            "price": 0.25,
            "change_1h": 12.5,
            "rvol": 6.2,
            "atr": 0.03,
            "resistance_gap": 2.5,
            "whale_buy": 1_500_000,
            "stablecoin_inflow": 2_000_000,
            "short_liquidations": 500_000,
            "project_age_days": 45,
            "legit_use_case": True,
            "organic_volume": True,
            "token_unlocks": False
        }

# 🔹 FINNHUB INDICATORS
def get_finnhub_indicators(ticker):
    rsi_data = fetch_json("https://finnhub.io/api/v1/indicator", {
        "symbol": ticker,
        "resolution": "D",
        "indicator": "rsi",
        "token": FINNHUB_KEY
    })
    return {
        "rsi": rsi_data.get("rsi", {}).get("value", 50),
        "macd_histogram": 1.2,
        "ema_stack": True,
        "ema_stack_5min": True,
        "ema_stack_1h": True,
        "vwap": 0.23,
        "vwap_5min": 0.22,
        "vwap_1h": 0.21,
        "stoch_rsi_crossover": True,
        "obv_confirmation": True
    }

# 🔹 LUNARCRUSH SENTIMENT
def get_lunarcrush_data(ticker):
    data = fetch_json("https://api.lunarcrush.com/v2", {
        "data": "assets",
        "key": LUNARCRUSH_KEY,
        "symbol": ticker.replace("USD", "")
    })
    asset = data.get("data", [{}])[0]
    return {
        "galaxyScore": asset.get("galaxy_score", 75),
        "social_volume_change": asset.get("twitter_mentions_percent_change", 60),
        "summary": "Strong bullish sentiment",
        "url": f"https://lunarcrush.com/coins/{ticker.replace('USD', '').lower()}"
    }

# 🔹 MESSARI CATALYSTS
def get_messari_news(ticker):
    data = fetch_json("https://data.messari.io/api/v1/news", {"filter": ticker})
    news = data.get("data", [{}])[0]
    return {
        "title": news.get("title", "Protocol upgrade announced"),
        "url": news.get("url", "https://messari.io/news")
    }

# 🔹 COINGLASS ORDERBOOK
def get_orderbook_data(ticker):
    data = fetch_json("https://open-api.coinglass.com/public/v2/open_interest", {
        "symbol": ticker
    }, headers={"coinglassSecret": COINGLASS_KEY})
    d = data.get("data", {})
    return {
        "wall": f"{d.get('totalOpenInterest', '0')} OI",
        "exchange": d.get("exchangeName", "Binance")
    }

# 🔹 SANTIMENT CORRELATION
def get_santiment_correlation(ticker):
    # Placeholder logic — real GraphQL query can be added
    return {
        "correlation": 0.82
    }

# 🔹 ORDERFLOW / DARK POOL
def get_orderflow_data(ticker):
    # Simulated data
    return {
        "dark_pool": 1_200_000
    }
