# notifier.py

import os
from alerts.telegram_dispatcher import send_telegram_alert
from alerts.discord_dispatcher import send_discord_alert
from alert_formatter import format_telegram, format_discord
from utils.logger import log

ADMIN_TELEGRAM_CHAT_ID = os.getenv("ADMIN_TELEGRAM_CHAT_ID")
ADMIN_DISCORD_WEBHOOK_URL = os.getenv("ADMIN_DISCORD_WEBHOOK_URL")

def notify_admin(message, level="info"):
    prefix = "⚠️" if level == "error" else "ℹ️"
    formatted_text = f"{prefix} *Admin Notification*\n\n{message}"

    try:
        send_telegram_alert({
            "text": formatted_text,
            "chat_id": ADMIN_TELEGRAM_CHAT_ID,
            "parse_mode": "Markdown"
        })
    except Exception as e:
        log(f"Admin Telegram error: {e}")

    try:
        embed = {
            "username": "EmeraldAlert Admin",
            "embeds": [{
                "title": f"{prefix} Admin Notification",
                "description": message,
                "color": 0xFFA500 if level == "error" else 0x00BFFF,
                "footer": {"text": "EmeraldAlert"},
            }]
        }
        send_discord_alert(embed, webhook_url=ADMIN_DISCORD_WEBHOOK_URL)
    except Exception as e:
        log(f"Admin Discord error: {e}")

def notify_failure(context, error):
    message = f"*Context:* {context}\n*Error:* `{str(error)}`"
    notify_admin(message, level="error")
