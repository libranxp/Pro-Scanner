# alerts/telegram.py
import requests
import os
from utils.logger import log

def send_telegram_alert(message, asset_type):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = {
        "crypto": os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID"),
        "stock": os.getenv("TELEGRAM_STOCK_CHANNEL_ID"),
    }.get(asset_type, os.getenv("TELEGRAM_CHAT_ID"))

    if not token or not chat_id:
        raise ValueError("Missing Telegram token or chat ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Telegram error: {response.text}")
