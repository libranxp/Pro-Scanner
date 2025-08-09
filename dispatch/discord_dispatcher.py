# discord_dispatcher.py

import os
import requests
from alert_formatter import format_discord
from utils.logger import log

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_alert(data, webhook_url=None):
    embed = format_discord(data)
    url = webhook_url or DISCORD_WEBHOOK_URL
    try:
        response = requests.post(url, json=embed)
        response.raise_for_status()
        log(f"✅ Discord alert sent for {data.get('ticker')}")
    except Exception as e:
        log(f"❌ Discord alert failed: {e}")
        raise
