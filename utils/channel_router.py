import os
import requests

# Load secrets from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")

def send_to_discord(message):
    payload = {
        "content": message
    }
    try:
        requests.post(DISCORD_WEBHOOK, json=payload, timeout=5)
    except Exception as e:
        print(f"[DISCORD ERROR] {e}")

def send_to_channel(channel, message):
    if channel == "telegram":
        send_to_telegram(message)
    elif channel == "discord":
        send_to_discord(message)
    else:
        print(f"[NO ROUTE] Channel '{channel}' not recognized. Message:\n{message}")
