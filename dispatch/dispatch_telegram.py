import os
import requests

def send_telegram(message: str, asset_type: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if asset_type == "stock":
        channel_id = os.getenv("TELEGRAM_STOCK_CHANNEL_ID")
    elif asset_type == "crypto":
        channel_id = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")
    elif asset_type == "admin":
        channel_id = os.getenv("TELEGRAM_ADMIN_CHANNEL_ID")
    elif asset_type == "dev":
        channel_id = os.getenv("TELEGRAM_DEV_CHANNEL_ID")
    else:
        channel_id = os.getenv("TELEGRAM_CHAT_ID")  # fallback

    if not token or not channel_id:
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": channel_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=payload)
