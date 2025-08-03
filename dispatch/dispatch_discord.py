import os
import requests
from alert_formatter import format_alert

DISCORD_STOCK_WEBHOOK = os.getenv("DISCORD_STOCK_WEBHOOK")
DISCORD_CRYPTO_WEBHOOK = os.getenv("DISCORD_CRYPTO_WEBHOOK")

def send_discord_message(webhook_url, message):
    payload = {"content": message}
    res = requests.post(webhook_url, json=payload)
    print(f"[Debug] Discord response status: {res.status_code}")
    res.raise_for_status()

def dispatch_alerts(validated_alerts):
    for asset in validated_alerts:
        print(f"[Debug] Dispatching alert for: {asset['symbol']} to Discord")
        message = format_alert(asset)
        webhook = (
            DISCORD_STOCK_WEBHOOK if asset["asset_type"].lower() == "stock"
            else DISCORD_CRYPTO_WEBHOOK
        )
        send_discord_message(webhook, message)
