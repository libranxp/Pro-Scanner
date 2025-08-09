import os
import requests
from utils.logger import log

TELEGRAM_CREDENTIALS = {
    "admin": {
        "token": os.getenv("TELEGRAM_BOT_TOKEN"),
        "chat_id": os.getenv("TELEGRAM_ADMIN_CHANNEL_ID")
    },
    "crypto": {
        "token": os.getenv("TELEGRAM_BOT_TOKEN"),
        "chat_id": os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")
    },
    "stock": {
        "token": os.getenv("TELEGRAM_BOT_TOKEN"),
        "chat_id": os.getenv("TELEGRAM_STOCK_CHANNEL_ID")
    },
    "dev": {
        "token": os.getenv("TELEGRAM_BOT_TOKEN"),
        "chat_id": os.getenv("TELEGRAM_DEV_CHANNEL_ID")
    }
}

def send_telegram_message(category: str, message: str):
    creds = TELEGRAM_CREDENTIALS.get(category)
    if not creds or not creds["token"] or not creds["chat_id"]:
        raise ValueError(f"Missing token or chat_id for category: {category}")

    url = f"https://api.telegram.org/bot{creds['token']}/sendMessage"
    payload = {"chat_id": creds["chat_id"], "text": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Telegram dispatch failed: {e}")
