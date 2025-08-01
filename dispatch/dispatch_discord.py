import os
import requests

def send_discord(message: str, asset_type: str):
    webhook_map = {
        "stock": "DISCORD_STOCK_WEBHOOK",
        "crypto": "DISCORD_CRYPTO_WEBHOOK",
        "catalyst": "DISCORD_CATALYST_WEBHOOK",
        "sentiment": "DISCORD_SENTIMENT_WEBHOOK",
        "status": "DISCORD_STATUS_WEBHOOK",
        "hotlist": "DISCORD_HOTLIST_WEBHOOK",
        "admin": "DISCORD_ADMIN_ERRORS_WEBHOOK"
    }

    webhook = os.getenv(webhook_map.get(asset_type, "DISCORD_STATUS_WEBHOOK"))
    if not webhook:
        return

    embed = {"embeds": [{"description": message}]}
    requests.post(webhook, json=embed)
