# dispatch/alert_dispatcher.py

import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.logger import log

# Replace with your actual tokens and channel IDs
TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
TELEGRAM_CHAT_ID = "your-telegram-chat-id"
DISCORD_WEBHOOK_URL = "your-discord-webhook-url"

def send_admin_alert(title: str, message: str, level: str = "info"):
    """
    Sends an admin alert to Telegram and Discord with BST timestamp.
    """
    bst_time = datetime.now(ZoneInfo("Europe/London")).strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{title}\n{message}\n\n🕒 Timestamp: {bst_time} BST"

    # Telegram
    try:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        telegram_payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": full_message,
            "parse_mode": "Markdown"
        }
        response = requests.post(telegram_url, json=telegram_payload)
        response.raise_for_status()
        log("📨 Admin alert sent to Telegram.")
    except Exception as e:
        log(f"⚠️ Failed to send Telegram alert: {e}")

    # Discord
    try:
        discord_payload = {
            "content": full_message
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=discord_payload)
        response.raise_for_status()
        log("📨 Admin alert sent to Discord.")
    except Exception as e:
        log(f"⚠️ Failed to send Discord alert: {e}")

def dispatch_alerts(alerts: list):
    """
    Dispatches a list of alerts to Telegram and Discord.
    Each alert should be a dictionary with 'title' and 'message'.
    """
    if not alerts:
        log("ℹ️ No alerts to dispatch.")
        return

    for alert in alerts:
        title = alert.get("title", "🚨 Alert")
        message = alert.get("message", "")
        send_admin_alert(title, message, level="info")
