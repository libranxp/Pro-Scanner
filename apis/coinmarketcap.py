import requests
import os
from apis.provider_registry import mark_provider_status
from utils.logger import log

def fetch_data():
    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        headers = {"X-CMC_PRO_API_KEY": os.getenv("CMC_KEY")}
        params = {"limit": 100, "convert": "USD"}
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        mark_provider_status("coinmarketcap", "online")
        return res.json()
    except Exception as e:
        mark_provider_status("coinmarketcap", "error")
        log(f"❌ CoinMarketCap fetch failed: {e}")
        raise
