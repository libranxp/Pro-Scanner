import requests
import os
from apis.provider_registry import mark_provider_status
from utils.logger import log

def fetch_social_metrics(symbol):
    try:
        url = f"https://api.lunarcrush.com/v2?data=assets&key={os.getenv('LUNARCRUSH_KEY')}&symbol={symbol}"
        res = requests.get(url)
        res.raise_for_status()
        mark_provider_status("lunarcrush", "online")
        return res.json()
    except Exception as e:
        mark_provider_status("lunarcrush", "error")
        log(f"❌ LunarCrush fetch failed for {symbol}: {e}")
        raise
