# alerts/discord.py
import requests
import os
from utils.logger import log

def send_discord_alert(message, asset_type):
    webhook = {
        "crypto": os.getenv("DISCORD_CRYPTO_WEBHOOK"),
        "stock": os.getenv("DISCORD_STOCK_WEBHOOK"),
    }.get(asset_type)

    if not webhook:
        raise ValueError("Missing Discord webhook for asset type")

    payload = {
        "content": message
    }

    response = requests.post(webhook, json=payload)
    if response.status_code >= 400:
        raise Exception(f"Discord error: {response.text}")

