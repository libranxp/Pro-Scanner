from alerts.alert_formatter import format_telegram
from utils.logger import log
import requests
import os

def send_telegram_alert(alert):
    try:
        formatted = format_telegram(alert)
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        channel_id = get_channel_id(alert)

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": channel_id,
            "text": formatted,
            "parse_mode": "Markdown"
        }

        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Telegram error: {response.text}")

        log(f"📨 Telegram alert sent for {alert.get('ticker')}")

    except Exception as e:
        log(f"❌ Telegram dispatch failed: {e}")
        raise

def get_channel_id(alert):
    if alert.get("type") == "crypto":
        return os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")
    elif alert.get("type") == "stock":
        return os.getenv("TELEGRAM_STOCK_CHANNEL_ID")
    else:
        return os.getenv("TELEGRAM_DEV_CHANNEL_ID")
