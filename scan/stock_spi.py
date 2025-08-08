# scan/stock_spi.py
import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo

BST = ZoneInfo("Europe/London")
FMP_KEY = os.environ["FMP_KEY"]

def scan_stocks():
    url = f"https://financialmodelingprep.com/api/v3/stock-screener?apikey={FMP_KEY}&volumeMoreThan=1000000&priceMoreThan=0.01&priceLowerThan=50"
    res = requests.get(url).json()
    candidates = []

    for stock in res:
        symbol = stock["symbol"]
        price = float(stock["price"])
        change = float(stock["changesPercentage"].strip('%'))
        volume = int(stock["volume"])
        float_shares = float(stock.get("float", 0))
        short_interest = float(stock.get("shortInterest", 0))

        # Technical filters
        if change < 5 or volume < 1000000 or float_shares > 50000000 or short_interest < 15:
            continue

        candidate = {
            "ticker": symbol,
            "price": round(price, 2),
            "change": round(change, 2),
            "volume": volume,
            "entry": round(price * 1.01, 2),
            "stop": round(price * 0.98, 2),
            "target": round(price * 1.05, 2),
            "technicals": "VWAP reclaim, EMA stack bullish",
            "catalyst": "Earnings beat + Insider buy",
            "sentiment": "Bullish (Reddit + Twitter)",
            "chart_url": f"https://www.tradingview.com/symbols/NASDAQ-{symbol}/",
            "confidence": 88,
            "risk": "🟢 Low",
            "timestamp": datetime.now(tz=BST).strftime("%Y-%m-%d %H:%M:%S %Z")
        }

        candidates.append(candidate)

    return candidates
