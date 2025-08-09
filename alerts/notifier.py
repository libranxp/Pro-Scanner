# notifier.py
from alerts.telegram import send_telegram_alert
from alerts.discord import send_discord_alert
from alerts.formatter import format_alert, format_admin_notice
from utils.logger import log

ADMIN_CHANNELS = {
    "telegram": "YOUR_ADMIN_TELEGRAM_ID",
    "discord": "YOUR_ADMIN_DISCORD_WEBHOOK"
}

def send_alerts(alerts):
    for alert in alerts:
        message = format_alert(alert)
        success = True

        try:
            send_telegram_alert(message)
        except Exception as e:
            log(f"Telegram error: {e}")
            success = False

        try:
            send_discord_alert(message)
        except Exception as e:
            log(f"Discord error: {e}")
            success = False

        if not success:
            notify_admin(f"Failed to deliver alert for {alert.get('ticker')}", level="error")

def notify_admin(message, level="info"):
    formatted = format_admin_notice(message, level)

    try:
        send_telegram_alert(formatted, chat_id=ADMIN_CHANNELS["telegram"])
    except Exception as e:
        log(f"Admin Telegram error: {e}")

    try:
        send_discord_alert(formatted, webhook_url=ADMIN_CHANNELS["discord"])
    except Exception as e:
        log(f"Admin Discord error: {e}")
