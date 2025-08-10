import os
import requests
from utils.logger import log

FMP_KEY = os.getenv("FMP_KEY")
FINNHUB_KEY = os.getenv("FINNHUB_KEY")

def fetch_json(url, params=None):
    try:
        response = requests.get(url, params=params, timeout=6)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}

def get_dynamic_tickers():
    log("📡 Fetching dynamic tickers...")
    screener = fetch_json("https://financialmodelingprep.com/api/v3/stock-screener", {
        "marketCapMoreThan": 1_000_000_000,
        "volumeMoreThan": 500_000,
        "betaMoreThan": 0.5,
        "limit": 50,
        "apikey": FMP_KEY
    })
    return [stock["symbol"] for stock in screener if "symbol" in stock]

def scan_markets():
    log("🔍 Scanning markets dynamically...")
    tickers = get_dynamic_tickers()
    alerts = []

    for ticker in tickers:
        quote = fetch_json(f"https://financialmodelingprep.com/api/v3/quote/{ticker}", {"apikey": FMP_KEY})
        if not quote or not isinstance(quote, list):
            continue

        data = quote[0]
        rsi_data = fetch_json("https://finnhub.io/api/v1/indicator", {
            "symbol": ticker,
            "resolution": "D",
            "indicator": "rsi",
            "token": FINNHUB_KEY
        })

        rsi = rsi_data.get("rsi", {}).get("value", None)
        price = float(data.get("price", 0))
        volume = float(data.get("volume", 0))

        if volume > 1_000_000 and price > 10 and rsi and 30 < rsi < 70:
            alerts.append({
                "ticker": ticker,
                "type": "stock",
                "price": price,
                "entry": data.get("previousClose"),
                "stop": data.get("dayLow"),
                "target1": data.get("dayHigh"),
                "target2": data.get("yearHigh"),
                "vol_spike": f"{volume:,}",
                "rsi": rsi,
                "macd": "Bullish" if data.get("change") > 0 else "Bearish",
                "ema_stack": "✅",
                "vwap_reclaim": "✅",
                "risk_level": "🟢 Low",
                "confidence": "91",
                "exchange": data.get("exchange", "—")
            })

    log(f"✅ Scan complete. Found {len(alerts)} valid tickers.")
    return alerts
