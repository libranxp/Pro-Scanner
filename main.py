# main.py
import sys
from core.execution_plan import run_scan
from alerts.alert_formatter import format_alert
from alerts.telegram import send_telegram_alert, send_admin_message
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
        log("🚀 Starting EmeraldAlert diagnostic scan...")

        # Send test messages to confirm delivery
        send_admin_message("🧪 EmeraldAlert test message: Telegram is working.")
        send_discord_alert("🧪 EmeraldAlert test message: Discord is working.", "stock")

        alerts = run_scan()
        log(f"📊 Raw alerts: {alerts}")

        if not alerts:
            log("⚠️ No qualifying alerts found.")
            send_admin_message("⚠️ No alerts found in this scan.")
            return

        log(f"🔍 Found {len(alerts)} alert(s). Dispatching...")

        for alert in alerts:
            ticker = alert.get("ticker", "UNKNOWN")
            confidence = alert.get("confidence", 0)
            message = format_alert(alert)
            asset_type = "crypto" if "USDT" in ticker else "stock"

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
