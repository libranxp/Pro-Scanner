import requests
import os
from apis.provider_registry import mark_provider_status
from utils.logger import log

def fetch_asset_metrics(asset_slug):
    try:
        url = f"https://data.messari.io/api/v1/assets/{asset_slug}/metrics"
        headers = {"x-messari-api-key": os.getenv("MESSARI_KEY")}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        mark_provider_status("messari", "online")
        return res.json()
    except Exception as e:
        mark_provider_status("messari", "error")
        log(f"❌ Messari fetch failed for {asset_slug}: {e}")
        raise
