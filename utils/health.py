from dispatch.alert_dispatcher import send_admin_alert
from utils.logger import log

def report_health():
    try:
        message = "✅ Alert system health check passed."
        send_admin_alert(message)
        log("🟢 Health check dispatched.")
    except Exception as e:
        log(f"❌ Health check failed: {e}")
        send_admin_alert(f"❌ Health check failed: {e}")

