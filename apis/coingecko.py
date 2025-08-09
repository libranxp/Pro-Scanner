import requests
from apis.provider_registry import mark_provider_status
from utils.logger import log

def fetch_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 100}
        res = requests.get(url, params=params)
        res.raise_for_status()
        mark_provider_status("coingecko", "online")
        return res.json()
    except Exception as e:
        mark_provider_status("coingecko", "error")
        log(f"❌ Coingecko fetch failed: {e}")
        raise
