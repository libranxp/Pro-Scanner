# alerts/discord.py
import requests
import os

WEBHOOKS = {
    "crypto": os.environ["DISCORD_CRYPTO_WEBHOOK"],
    "stock": os.environ["DISCORD_STOCK_WEBHOOK"],
}

def send_discord_alert(message, asset_type):
    webhook_url = WEBHOOKS.get(asset_type, os.environ["DISCORD_ADMIN_ERRORS_WEBHOOK"])
    payload = {"content": message}
    requests.post(webhook_url, json=payload)

