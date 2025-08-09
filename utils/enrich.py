import os
import requests
from datetime import datetime

# Load secrets
ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE_KEY")
FINNHUB_KEY = os.getenv("FINNHUB_KEY")
MESSARI_KEY = os.getenv("MESSARI_API_KEY")
SANTIMENT_KEY = os.getenv("SANTIMENT_API_KEY")
LUNARCRUSH_KEY = os.getenv("LUNARCRUSH_KEY")
FMP_KEY = os.getenv("FMP_KEY")
CMC_KEY = os.getenv("CMC_KEY")
COINGLASS_KEY = os.getenv("COINGLASS_KEY")

def fetch_json(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=6)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}

def get_price_data(ticker):
    # Primary: FMP
    fmp = fetch_json(f"https://financialmodelingprep.com/api/v3/quote/{ticker}", {"apikey": FMP_KEY})
    if fmp and isinstance(fmp, list):
        info = fmp[0]
        return {
            "price": f"${info.get('price', 0):.2f}",
            "entry": f"${info.get('previousClose', 0):.2f}",
            "stop": f"${info.get('dayLow', 0):.2f}",
            "target1": f"${info.get('dayHigh', 0):.2f}",
            "target2": f"${info.get('yearHigh', 0):.2f}"
        }

    # Fallback: AlphaVantage
    av = fetch_json("https://www.alphavantage.co/query", {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": ALPHAVANTAGE_KEY
    })
    quote = av.get("Global Quote", {})
    return {
        "price": f"${float(quote.get('05. price', 0)):.2f}",
        "entry": f"${float(quote.get('08. previous close', 0)):.2f}",
        "stop": f"${float(quote.get('04. low', 0)):.2f}",
        "target1": f"${float(quote.get('03. high', 0)):.2f}",
        "target2": f"${float(quote.get('03. high', 0)):.2f}"
    }

def get_sentiment(ticker):
    lc = fetch_json("https://api.lunarcrush.com/v2", {
        "data": "assets",
        "key": LUNARCRUSH_KEY,
        "symbol": ticker
    })
    asset = lc.get("data", [{}])[0]
    return {
        "sentiment_analysis": f"Galaxy Score: {asset.get('galaxy_score', '—')}",
        "sentiment_surge": f"{asset.get('twitter_mentions_percent_change', '—')}% Twitter mentions",
        "sentiment_link": f"https://lunarcrush.com/coins/{ticker.lower()}"
    }

def get_catalyst(ticker):
    messari = fetch_json("https://data.messari.io/api/v1/news", {
        "key": MESSARI_KEY,
        "filter": ticker
    })
    news = messari.get("data", [{}])[0]
    return {
        "catalyst": news.get("title", "—"),
        "catalyst_link": news.get("url", "https://messari.io/news"),
        "catalyst_link_text": "Messari"
    }

def get_orderbook(ticker):
    cg = fetch_json("https://open-api.coinglass.com/public/v2/open_interest", {
        "symbol": ticker
    }, headers={"coinglassSecret": COINGLASS_KEY})
    data = cg.get("data", {})
    return {
        "orderbook_wall": f"{data.get('totalOpenInterest', '—')} OI",
        "orderbook_exchange": data.get("exchangeName", "—")
    }

def get_santiment(ticker):
    san = fetch_json(f"https://api.santiment.net/graphql", headers={
        "Authorization": f"Apikey {SANTIMENT_KEY}"
    })
    # Placeholder — real GraphQL query needed
    return {
        "btc_correlation": "—",
        "dev_activity": "—"
    }

def enrich_alert_data(raw):
    ticker = raw.get("ticker", "")
    asset_type = raw.get("asset_type", "Crypto USD Pair" if "USD" in ticker else "US Stock")

    price = get_price_data(ticker)
    sentiment = get_sentiment(ticker)
    catalyst = get_catalyst(ticker)
    orderbook = get_orderbook(ticker)
    santiment = get_santiment(ticker)

    return {
        "ticker": ticker,
        "asset_type": asset_type,
        **price,
        "vol_spike": raw.get("vol_spike", "—"),
        "rsi": raw.get("rsi", "—"),
        "macd": raw.get("macd", "—"),
        "ema_stack": raw.get("ema_stack", "—"),
        "vwap_reclaim": raw.get("vwap_reclaim", "—"),
        **orderbook,
        **santiment,
        "exchange": raw.get("exchange", "—"),
        **sentiment,
        **catalyst,
        "risk_level": raw.get("risk_level", "—"),
        "confidence": raw.get("confidence", "—"),
        "chart_link": f"https://www.tradingview.com/symbols/{ticker.replace('/', '')}",
        "timestamp": raw.get("timestamp", datetime.utcnow().strftime("%Y-%m-%d %H:%M")),
        "type": raw.get("type", "crypto").lower()
    }
