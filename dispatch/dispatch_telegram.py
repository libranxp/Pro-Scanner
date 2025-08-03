import sys
import os

# Add root directory to sys.path to access dispatch.alert_formatter
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dispatch.alert_formatter import format_alert
import requests

def send_telegram_message(message: str):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[Telegram] Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"[Telegram] Failed to send message: {response.text}")
        else:
            print("[Telegram] Message sent successfully.")
    except Exception as e:
        print(f"[Telegram] Error sending message: {e}")


