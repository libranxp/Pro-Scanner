import json
import os
import sys
from alert_formatter import format_alert
from dispatch.dispatch_telegram import send_telegram_message
from dispatch.dispatch_discord import send_discord_message

# Load config threshold
THRESHOLD = int(os.getenv("ALERT_SCORE_THRESHOLD", "75"))

# Load scan results
def load_alerts(path="logs/scan_history.json"):
    if not os.path.exists(path):
        print("[Validation] scan_history.json not found.")
        return []
    with open(path) as f:
        return json.load(f)

def validate_alerts(alerts):
    validated = []
    for asset in alerts:
        score = asset.get("score", 0)
        if score >= THRESHOLD:
            validated.append(asset)
    print(f"[Validation] {len(validated)} alerts passed score threshold of {THRESHOLD}.")
    return validated

def dispatch(validated_alerts):
    for asset in validated_alerts:
        try:
            print(f"[Dispatch] Sending alert for {asset['symbol']}...")
            message = format_alert(asset)
            send_telegram_message(message)
            webhook = (
                os.getenv("DISCORD_STOCK_WEBHOOK") if asset["asset_type"] == "stock"
                else os.getenv("DISCORD_CRYPTO_WEBHOOK")
            )
            send_discord_message(webhook, message)
        except Exception as e:
            print(f"[Error] Failed to dispatch {asset['symbol']}: {e}")

def main():
    alerts = load_alerts()
    if not alerts:
        print("[Validation] No alerts found.")
        sys.exit(0)
    valid = validate_alerts(alerts)
    if not valid:
        print("[Validation] No alerts passed score filter.")
        sys.exit(0)
    dispatch(valid)

if __name__ == "__main__":
    main()
