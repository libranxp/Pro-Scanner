# main.py
from core.execution_plan import run_scan
from alerts.alert_formatter import format_alert
from alerts.telegram import send_telegram_alert
from alerts.discord import send_discord_alert

def main():
    alerts = run_scan()
    for alert in alerts:
        message = format_alert(alert)
        asset_type = "crypto" if "USDT" in alert["ticker"] else "stock"
        send_telegram_alert(message, asset_type)
        send_discord_alert(message, asset_type)

if __name__ == "__main__":
    main()
