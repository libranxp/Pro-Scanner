import os
import requests

def send_telegram_message(message: str):
    chat_id = os.getenv("TELEGRAM_ADMIN_CHANNEL_ID")  # ✅ default fallback channel
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token or not chat_id:
        print("[Telegram] Missing credentials.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        res = requests.post(url, json=payload)
        if res.status_code != 200:
            print(f"[Telegram] Dispatch failed: {res.text}")
    except Exception as e:
        print(f"[Telegram] Error: {e}")
