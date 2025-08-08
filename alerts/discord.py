# alerts/discord.py
import requests
import os

WEBHOOKS = {
    "crypto": os.environ["DISCORD_CRYPTO_WEBHOOK"],
    "stock": os.environ["DISCORD_STOCK_WEBHOOK"],
}

def send_discord_alert(message, channel="crypto"):
    webhook_url = WEBHOOKS[channel]
    payload = {"content": message}
    requests.post(webhook_url, json=payload)
