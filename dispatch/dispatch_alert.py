import os
import requests
from utils.logger import log
from utils.enrich import enrich_alert_data

# Telegram channels
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNELS = {
    "crypto": os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID"),
    "stock": os.getenv("TELEGRAM_STOCK_CHANNEL_ID"),
    "catalyst": os.getenv("TELEGRAM_DEV_CHANNEL_ID"),
    "sentiment": os.getenv("TELEGRAM_DEV_CHANNEL_ID"),
    "hotlist": os.getenv("TELEGRAM_DEV_CHANNEL_ID"),
    "status": os.getenv("TELEGRAM_ADMIN_CHANNEL_ID"),
    "error": os.getenv("TELEGRAM_ADMIN_CHANNEL_ID"),
}

# Discord webhooks
DISCORD_WEBHOOKS = {
    "crypto": os.getenv("DISCORD_CRYPTO_WEBHOOK"),
    "stock": os.getenv("DISCORD_STOCK_WEBHOOK"),
    "catalyst": os.getenv("DISCORD_CATALYST_WEBHOOK"),
    "sentiment": os.getenv("DISCORD_SENTIMENT_WEBHOOK"),
    "hotlist": os.getenv("DISCORD_HOTLIST_WEBHOOK"),
    "status": os.getenv("DISCORD_STATUS_WEBHOOK"),
    "error": os.getenv("DISCORD_ADMIN_ERRORS_WEBHOOK"),
}

def format_alert(alert):
    # Same formatting logic as before
    # Use alert["type"] to determine layout
    ...

def send_telegram_alert(alert, alert_type):
    channel_id = TELEGRAM_CHANNELS.get(alert_type)
    if not TELEGRAM_BOT_TOKEN or not channel_id:
        log(f"❌ Telegram routing failed for type: {alert_type}")
        return

    message = format_alert(alert)
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": channel_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    response = requests.post(url, json=payload)
    log(f"📤 Telegram [{alert_type}] status: {response.status_code}")
    log(f"📤 Telegram response: {response.text}")

def send_discord_alert(alert, alert_type):
    webhook = DISCORD_WEBHOOKS.get(alert_type)
    if not webhook:
        log(f"❌ Discord routing failed for type: {alert_type}")
        return

    message = format_alert(alert)
    payload = {"content": message}

    response = requests.post(webhook, json=payload)
    log(f"📤 Discord [{alert_type}] status: {response.status_code}")
    log(f"📤 Discord response: {response.text}")

def dispatch_alerts(alerts):
    if not alerts:
        log("ℹ️ No alerts to dispatch.")
        return

    log(f"📊 Dispatching {len(alerts)} alerts...")

    for raw_alert in alerts:
        enriched = enrich_alert_data(raw_alert)
        alert_type = enriched.get("type", "crypto").lower()

        send_telegram_alert(enriched, alert_type)
        send_discord_alert(enriched, alert_type)
