import os
import sys
import requests

# Add repo root to system path (optional but helpful for some workflows)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dispatch.alert_formatter import format_alert  # Adjusted import

# Webhook URLs from environment variables
DISCORD_STOCK_WEBHOOK = os.getenv("DISCORD_STOCK_WEBHOOK")
DISCORD_CRYPTO_WEBHOOK = os.getenv("DISCORD_CRYPTO_WEBHOOK")

def send_discord(message, asset_type):
    """
    Routes a formatted alert message to the appropriate Discord channel.
    """
    webhook_url = (
        DISCORD_STOCK_WEBHOOK if asset_type.lower() == "stock"
        else DISCORD_CRYPTO_WEBHOOK
    )

    payload = {"content": message}
    res = requests.post(webhook_url, json=payload)
    print(f"[Debug] Discord response status: {res.status_code}")
    res.raise_for_status()

def dispatch_alerts(validated_alerts):
    """
    Iterates through validated alerts and dispatches each one to Discord.
    """
    for asset in validated_alerts:
        print(f"[Debug] Dispatching alert for: {asset['symbol']} to Discord")
        message = format_alert(asset)
        send_discord(message, asset["asset_type"])
