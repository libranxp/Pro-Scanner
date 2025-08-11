import requests
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_to_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)
    print(f"[TELEGRAM] Status {response.status_code} | {response.text}")

def send_to_discord(message):
    if not DISCORD_WEBHOOK:
        raise ValueError("Missing DISCORD_WEBHOOK")

    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK, json=payload)
    print(f"[DISCORD] Status {response.status_code} | {response.text}")

def send_to_channel(channel, message):
    if channel == "telegram":
        send_to_telegram(message)
    elif channel == "discord":
        send_to_discord(message)
    else:
        raise ValueError(f"Unknown channel: {channel}")
