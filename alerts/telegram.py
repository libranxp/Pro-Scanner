# alerts/telegram.py
import requests
import os

CHANNEL_IDS = {
    "crypto": os.environ["TELEGRAM_CRYPTO_CHANNEL_ID"],
    "stock": os.environ["TELEGRAM_STOCK_CHANNEL_ID"],
}

def send_telegram_alert(message, asset_type):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = CHANNEL_IDS.get(asset_type, os.environ["TELEGRAM_ADMIN_CHANNEL_ID"])
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)
