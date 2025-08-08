# main.py
import sys
from core.execution_plan import run_scan
from alerts.alert_formatter import format_alert
from alerts.telegram import send_telegram_alert, send_admin_message, check_for_commands
from alerts.discord import send_discord_alert
from utils.logger import log
import os
import requests

def report_admin_error(message):
    webhook = os.getenv("DISCORD_ADMIN_ERRORS_WEBHOOK")
    if webhook:
        try:
            requests.post(webhook, json={"content": f"🚨 EmeraldAlert Error:\n{message}"})
        except Exception as e:
            log(f"❌ Failed to report admin error: {e}")

def main():
    try:
        # Check for Telegram command
        command = check_for_commands()
        force_send = "--force" in sys.argv or command == "scan"
        dry_run = "--dry" in sys.argv or command == "dry"

        log("🚀 Starting EmeraldAlert scan...")
        alerts = run_scan()

        log(f"📊 Raw alerts: {alerts}")

        if not alerts:
            log("⚠️ No qualifying alerts found.")
            send_admin_message("⚠️ No alerts found in this scan.")
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
                send_admin_message(f"[DRY RUN] Would send alert for {ticker}")
                continue

            try:
                send_telegram_alert(message, asset_type)
                send_discord_alert(message, asset_type)
                log(f"✅ Alert sent for {ticker}")
            except Exception as e:
                log(f"❌ Failed to send alert for {ticker}: {e}")
                report_admin_error(f"Failed to send alert for {ticker}: {e}")

    except Exception as e:
        log(f"🔥 Fatal error: {e}")
        report_admin_error(f"Fatal error in EmeraldAlert: {e}")
        send_admin_message(f"🔥 Fatal error: {e}")

if __name__ == "__main__":
    main()
