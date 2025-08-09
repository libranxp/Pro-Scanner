# telegram_dispatcher.py

import os
import requests
from alert_formatter import format_telegram
from utils.logger import log

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(data):
    message = format_telegram(data)
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        log(f"✅ Telegram alert sent for {data.get('ticker')}")
    except Exception as e:
        log(f"❌ Telegram alert failed: {e}")
        raise
