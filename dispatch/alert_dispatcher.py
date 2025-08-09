# dispatch/alert_dispatcher.py

from alerts.alert_formatter import enrich_alert_data
from dispatch.telegram_dispatcher import send_telegram_alert
from dispatch.discord_dispatcher import send_discord_alert
from dispatch.validator import validate_alerts
from dispatch.notifier import notify_failure
from utils.logger import log

def dispatch_alerts(raw_alerts):
    try:
        valid_alerts = validate_alerts(raw_alerts)
        if not valid_alerts:
            log("⚠️ No valid alerts to dispatch.")
            return

        for alert in valid_alerts:
            enriched = enrich_alert_data(alert)
            try:
                send_telegram_alert(enriched)
                send_discord_alert(enriched)
            except Exception as e:
                notify_failure(f"Dispatch failed for {alert.get('ticker')}", e)

    except Exception as e:
        notify_failure("Alert validation or dispatch pipeline failed", e)
