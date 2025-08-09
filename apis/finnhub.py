import requests
import os
from apis.provider_registry import mark_provider_status
from utils.logger import log

def fetch_quote(symbol):
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={os.getenv('FINNHUB_KEY')}"
        res = requests.get(url)
        res.raise_for_status()
        mark_provider_status("finnhub", "online")
        return res.json()
    except Exception as e:
        mark_provider_status("finnhub", "error")
        log(f"❌ Finnhub fetch failed for {symbol}: {e}")
        raise
