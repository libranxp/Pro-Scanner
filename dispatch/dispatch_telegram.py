import os
import requests
from alert_formatter import format_alert

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    res = requests.post(url, json=payload)
    print(f"[Debug] Telegram response status: {res.status_code}")
    res.raise_for_status()

def dispatch_alerts(validated_alerts):
    for asset in validated_alerts:
        print(f"[Debug] Dispatching alert for: {asset['symbol']} to Telegram")
        message = format_alert(asset)
        send_telegram_message(message)

