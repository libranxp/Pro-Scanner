import requests
import os
from apis.provider_registry import mark_provider_status
from utils.logger import log

def fetch_stock_screener():
    try:
        url = "https://financialmodelingprep.com/api/v3/stock-screener"
        params = {
            "marketCapMoreThan": 100_000_000,
            "volumeMoreThan": 500_000,
            "priceMoreThan": 5,
            "apikey": os.getenv("FMP_KEY")
        }
        res = requests.get(url, params=params)
        res.raise_for_status()
        mark_provider_status("fmp", "online")
        return res.json()
    except Exception as e:
        mark_provider_status("fmp", "error")
        log(f"❌ FMP fetch failed: {e}")
        raise

