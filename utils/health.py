from dispatch.alert_dispatcher import send_admin_alert
from utils.logger import log

def report_health(success=True, error=None):
    if success:
        message = "✅ Alert system health check passed."
    else:
        message = f"❌ Alert system health check failed: {error}"

    try:
        send_admin_alert(message)
        log(f"📤 Health report sent: {message}")
    except Exception as e:
        log(f"❌ Failed to send health report: {e}")


