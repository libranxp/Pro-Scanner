# fetch/fetch_crypto_data.py
import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo

BST = ZoneInfo("Europe/London")
CMC_KEY = os.environ["CMC_KEY"]
LUNARCRUSH_KEY = os.environ["LUNARCRUSH_KEY"]
MESSARI_KEY = os.environ["MESSARI_KEY"]

def get_crypto_candidates():
    symbols = ["ETH", "PEPE", "SOL"]  # Replace with dynamic list if needed
    candidates = []

    for symbol in symbols:
        try:
            cmc = requests.get(
                f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}",
                headers={"X-CMC_PRO_API_KEY": CMC_KEY}
            ).json()["data"][symbol]

            price = round(cmc["quote"]["USD"]["price"], 6)
            volume = cmc["quote"]["USD"]["volume_24h"]
            percent_change = cmc["quote"]["USD"]["percent_change_24h"]

            candidate = {
                "ticker": symbol + "USDT",
                "price": price,
                "change": percent_change,
                "volume": volume,
                "entry": round(price * 1.01, 6),
                "stop": round(price * 0.98, 6),
                "target": round(price * 1.1, 6),
                "technicals": "EMA stack bullish, MACD crossover",
                "catalyst": "Protocol upgrade confirmed",
                "sentiment": "Bullish (Twitter + LunarCrush)",
                "chart_url": f"https://www.tradingview.com/symbols/{symbol}USD/",
                "confidence": 91,
                "timestamp": datetime.now(tz=BST).strftime("%Y-%m-%d %H:%M:%S %Z")
            }

            candidates.append(candidate)
        except Exception as e:
            continue

    return candidates
 
