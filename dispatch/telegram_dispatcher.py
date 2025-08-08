import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CHANNEL_MAP = {
    "crypto": os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID"),
    "stocks": os.getenv("TELEGRAM_STOCK_CHANNEL_ID"),
    "admin": os.getenv("TELEGRAM_ADMIN_CHANNEL_ID"),
    "debug": os.getenv("TELEGRAM_DEBUG_CHANNEL_ID"),
}

def send_telegram_message(category: str, message: str, parse_mode: str = "Markdown"):
    chat_id = CHANNEL_MAP.get(category)
    if not TELEGRAM_BOT_TOKEN or not chat_id:
        raise ValueError(f"Missing token or chat_id for category: {category}")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }

    response = requests.post(url, json=payload)
    if not response.ok:
        raise RuntimeError(f"Telegram send failed: {response.text}")
    return response.json()
