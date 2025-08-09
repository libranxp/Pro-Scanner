import requests
import os
from apis.provider_registry import mark_provider_status
from utils.logger import log

def fetch_data():
    try:
        url = "https://open-api.coinglass.com/public/v2/open_interest"
        headers = {"coinglassSecret": os.getenv("COINGLASS_KEY")}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        mark_provider_status("coinglass", "online")
        return res.json()
    except Exception as e:
        mark_provider_status("coinglass", "error")
        log(f"❌ Coinglass fetch failed: {e}")
        raise
