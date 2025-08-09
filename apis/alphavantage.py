import requests
import os
from apis.provider_registry import mark_provider_status
from utils.logger import log

def fetch_intraday(symbol):
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "5min",
            "apikey": os.getenv("ALPHAVANTAGE_KEY")
        }
        res = requests.get(url, params=params)
        res.raise_for_status()
        mark_provider_status("alpha_vantage", "online")
        return res.json()
    except Exception as e:
        mark_provider_status("alpha_vantage", "error")
        log(f"❌ Alpha Vantage fetch failed for {symbol}: {e}")
        raise
