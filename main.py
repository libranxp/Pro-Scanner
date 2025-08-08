# main.py
import sys
from core.execution_plan import run_scan
from alerts.alert_formatter import format_alert
from alerts.telegram import send_telegram_alert
from alerts.discord import send_discord_alert
from utils.logger import log

def main():
    force_send = "--force" in sys.argv

    log("Starting EmeraldAlert scan...")
    alerts = run_scan()

    if not alerts:
        log("No qualifying alerts found.")
        return

    log(f"Found {len(alerts)} alert(s). Dispatching...")

    for alert in alerts:
        if not force_send and alert.get("confidence", 0) < 70:
            log(f"Skipping {alert['ticker']} — confidence too low ({alert['confidence']}%)")
            continue

        message = format_alert(alert)
        asset_type = "crypto" if "USDT" in alert["ticker"] else "stock"

        try:
            send_telegram_alert(message, asset_type)
            send_discord_alert(message, asset_type)
            log(f"✅ Alert sent for {alert['ticker']}")
        except Exception as e:
            log(f"❌ Failed to send alert for {alert['ticker']}: {e}")

if __name__ == "__main__":
    main()
