# dispatch/discord_dispatcher.py
import os
import requests
from utils.logger import log

WEBHOOKS = {
    "crypto": os.getenv("DISCORD_CRYPTO_WEBHOOK"),
    "stocks": os.getenv("DISCORD_STOCKS_WEBHOOK"),
    "admin": os.getenv("DISCORD_ADMIN_WEBHOOK"),
}

def send_discord_alert(message: str, channel: str = "crypto"):
    webhook_url = WEBHOOKS.get(channel)
    if not webhook_url:
        log(f"⚠️ No Discord webhook configured for channel: {channel}")
        return

    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 204:
            log(f"❌ Discord error {response.status_code}: {response.text}")
    except Exception as e:
        log(f"❌ Discord dispatch failed: {e}")
