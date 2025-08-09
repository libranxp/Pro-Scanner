import os
import requests
from utils.formatters import format_telegram, format_discord
from utils.enrich import enrich_alert_data
from utils.logger import log

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")
DISCORD_WEBHOOK = os.getenv("DISCORD_CRYPTO_WEBHOOK")

def send_telegram_alert(alert):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHANNEL_ID:
        log("⚠️ Telegram credentials missing.")
        return

    message = format_telegram(alert)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)
    log(f"📤 Telegram response: {response.status_code} — {response.text}")

def send_discord_alert(alert):
    if not DISCORD_WEBHOOK:
        log("⚠️ Discord webhook missing.")
        return

    message = format_discord(alert)
    payload = {"content": message}

    response = requests.post(DISCORD_WEBHOOK, json=payload)
    log(f"📤 Discord response: {response.status_code} — {response.text}")

def dispatch_alerts(alerts):
    if not alerts:
        log("ℹ️ No alerts to dispatch.")
        return

    log(f"📊 Dispatching {len(alerts)} alerts...")

    for raw_alert in alerts:
        enriched = enrich_alert_data(raw_alert)
        send_telegram_alert(enriched)
        send_discord_alert(enriched)
