# dispatch/alert_dispatcher.py

import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.logger import log

# Admin channels
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADMIN_CHANNEL_ID = os.getenv("TELEGRAM_ADMIN_CHANNEL_ID")
DISCORD_ADMIN_ERRORS_WEBHOOK = os.getenv("DISCORD_ADMIN_ERRORS_WEBHOOK")

def send_admin_alert(title: str, message: str, level: str = "info"):
    """
    Sends an admin alert to Telegram and Discord with BST timestamp.
    """
    bst_time = datetime.now(ZoneInfo("Europe/London")).strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{title}\n{message}\n\n🕒 Timestamp: {bst_time} BST"

    # Telegram
    if TELEGRAM_BOT_TOKEN and TELEGRAM_ADMIN_CHANNEL_ID:
        try:
            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            telegram_payload = {
                "chat_id": TELEGRAM_ADMIN_CHANNEL_ID,
                "text": full_message,
                "parse_mode": "Markdown"
            }
            response = requests.post(telegram_url, json=telegram_payload)
            response.raise_for_status()
            log("📨 Admin alert sent to Telegram.")
        except Exception as e:
            log(f"⚠️ Failed to send Telegram admin alert: {e}")

    # Discord
    if DISCORD_ADMIN_ERRORS_WEBHOOK:
        try:
            discord_payload = {"content": full_message}
            response = requests.post(DISCORD_ADMIN_ERRORS_WEBHOOK, json=discord_payload)
            response.raise_for_status()
            log("📨 Admin alert sent to Discord.")
        except Exception as e:
            log(f"⚠️ Failed to send Discord admin alert: {e}")
