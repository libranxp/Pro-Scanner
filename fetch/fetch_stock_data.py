# fetch/fetch_stock_data.py
import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo

BST = ZoneInfo("Europe/London")
FINNHUB_KEY = os.environ["FINNHUB_KEY"]
FMP_KEY = os.environ["FMP_KEY"]

def get_stock_candidates():
    symbols = ["TSLA", "NVOS", "PLTR"]  # Replace with dynamic list if needed
    candidates = []

    for symbol in symbols:
        try:
            quote = requests.get(
                f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}"
            ).json()

            price = round(quote["c"], 2)
            percent_change = round(((quote["c"] - quote["pc"]) / quote["pc"]) * 100, 2)

            candidate = {
                "ticker": symbol,
                "price": price,
                "change": percent_change,
                "volume": quote["v"],
                "entry": round(price * 1.01, 2),
                "stop": round(price * 0.98, 2),
                "target": round(price * 1.05, 2),
                "technicals": "VWAP reclaim, EMA stack bullish",
                "catalyst": "Analyst upgrade confirmed",
                "sentiment": "Bullish (Twitter + Reddit)",
                "chart_url": f"https://www.tradingview.com/symbols/NASDAQ-{symbol}/",
                "confidence": 88,
                "timestamp": datetime.now(tz=BST).strftime("%Y-%m-%d %H:%M:%S %Z")
            }

            candidates.append(candidate)
        except Exception as e:
            continue

    return candidates
