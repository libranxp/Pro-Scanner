from dispatch.alert_dispatcher import send_admin_alert
from utils.logger import log

def report_health(success=True, error=None):
    if success:
        message = "✅ EmeraldAlert scan completed successfully."
    else:
        message = f"❌ EmeraldAlert scan failed:\n\n{error}"

    try:
        send_admin_alert(message)
        log(f"📤 Health report sent: {message}")
    except Exception as e:
        log(f"❌ Failed to send health report: {e}")
