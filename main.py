# main.py
import sys
from core.execution_plan import run_scan
from alerts.alert_formatter import format_alert
from alerts.telegram import send_telegram_alert
from alerts.discord import send_discord_alert
from utils.logger import log
import os

def main():
    force_send = "--force" in sys.argv
    dry_run = "--dry" in sys.argv

    log("🚀 Starting EmeraldAlert scan...")
    alerts = run_scan()

    log(f"📊 Raw alerts: {alerts}")

    if not alerts:
        log("⚠️ No qualifying alerts found.")
        return

    log(f"🔍 Found {len(alerts)} alert(s). Evaluating...")

    for alert in alerts:
        ticker = alert.get("ticker", "UNKNOWN")
        confidence = alert.get("confidence", 0)

        if not force_send and confidence < 70:
            log(f"⏭️ Skipping {ticker} — confidence too low ({confidence}%)")
            continue

        message = format_alert(alert)
        asset_type = "crypto" if "USDT" in ticker else "stock"

        if dry_run:
            log(f"[DRY RUN] Would send alert for {ticker}: {message}")
            continue

        try:
            send_telegram_alert(message, asset_type)
            send_discord_alert(message, asset_type)
            log(f"✅ Alert sent for {ticker}")
        except Exception as e:
            log(f"❌ Failed to send alert for {ticker}: {e}")

if __name__ == "__main__":
    main()
