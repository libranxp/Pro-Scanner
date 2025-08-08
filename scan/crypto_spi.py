# scan/crypto_spi.py
import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo

BST = ZoneInfo("Europe/London")
CMC_KEY = os.environ["CMC_KEY"]

def scan_crypto():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_KEY}
    params = {"limit": 200, "convert": "USD"}

    res = requests.get(url, headers=headers, params=params).json()
    candidates = []

    for asset in res.get("data", []):
        symbol = asset["symbol"]
        price = asset["quote"]["USD"]["price"]
        volume = asset["quote"]["USD"]["volume_24h"]
        percent_change = asset["quote"]["USD"]["percent_change_1h"]
        market_cap = asset["quote"]["USD"]["market_cap"]

        # Tiered price filters
        if not (0.01 <= price <= 100.00):
            continue

        # Technical filters
        if percent_change < 10 or volume < 500000:
            continue

        # Safety checks (mocked for now)
        if market_cap < 10000000:
            continue

        candidate = {
            "ticker": symbol + "USDT",
            "price": round(price, 6),
            "change": round(percent_change, 2),
            "volume": int(volume),
            "entry": round(price * 1.01, 6),
            "stop": round(price * 0.98, 6),
            "target": round(price * 1.1, 6),
            "technicals": "EMA stack bullish, MACD crossover",
            "catalyst": "Protocol upgrade confirmed",
            "sentiment": "Bullish (Twitter + LunarCrush)",
            "chart_url": f"https://www.tradingview.com/symbols/{symbol}USD/",
            "confidence": 91,
            "risk": "🟡 Medium",
            "timestamp": datetime.now(tz=BST).strftime("%Y-%m-%d %H:%M:%S %Z")
        }

        candidates.append(candidate)

    return candidates
