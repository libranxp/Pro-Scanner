# dispatch/discord_dispatcher.py

from alerts.alert_formatter import format_discord
from utils.logger import log
import requests
import os

def send_discord_alert(alert):
    try:
        payload = format_discord(alert)
        webhook_url = get_webhook_url(alert)

        response = requests.post(webhook_url, json=payload)
        if response.status_code != 204:
            raise Exception(f"Discord error: {response.text}")

        log(f"📨 Discord alert sent for {alert.get('ticker')}")

    except Exception as e:
        log(f"❌ Discord dispatch failed: {e}")
        raise

def get_webhook_url(alert):
    if alert.get("type") == "crypto":
        return os.getenv("DISCORD_CRYPTO_WEBHOOK")
    elif alert.get("type") == "stock":
        return os.getenv("DISCORD_STOCK_WEBHOOK")
    else:
        return os.getenv("DISCORD_DEV_WEBHOOK")
