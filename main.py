# main.py
import os
import sys
from datetime import datetime
from alerts.scanner import scan_markets
from alerts.validator import validate_alerts
from alerts.formatter import format_alert
from dispatch.telegram_dispatcher import send_telegram_message
from dispatch.discord_dispatcher import send_discord_alert  # Optional
from utils.logger import log  # If you have a logging utility

def main():
    force_send = "--force" in sys.argv
    dry_run = "--dry" in sys.argv

    log("🚀 EmeraldAlert scan started.")
    raw_alerts = scan_markets()
    log(f"📊 Raw alerts found: {len(raw_alerts)}")

    validated = validate_alerts(raw_alerts)
    log(f"✅ Validated alerts: {len(validated)}")

    if not validated:
        send_telegram_message("admin", "⚠️ No qualifying alerts found.")
        return

    for alert in validated:
        ticker = alert.get("ticker", "UNKNOWN")
        confidence = alert.get("confidence", 0)
        asset_type = alert.get("type", "stocks")  # "crypto" or "stocks"
        message = format_alert(alert)

        if not force_send and confidence < 70:
            log(f"⏭️ Skipping {ticker} — confidence too low ({confidence}%)")
            continue

        if dry_run:
            log(f"[DRY RUN] Would send alert for {ticker}")
            send_telegram_message("debug", f"[DRY RUN] {message}")
            continue

        try:
            send_telegram_message(asset_type, message)
            send_discord_alert(message, asset_type)  # Optional
            log(f"✅ Alert sent for {ticker}")
        except Exception as e:
            log(f"❌ Failed to send alert for {ticker}: {e}")
            send_telegram_message("admin", f"❌ Alert failed for {ticker}: {e}")

    log("✅ EmeraldAlert scan complete.")

if __name__ == "__main__":
    main()
