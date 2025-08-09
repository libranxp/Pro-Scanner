# utils/health.py

from utils.logger import log
from dispatch.alert_dispatcher import send_admin_alert

def report_health(success: bool = True, error: str = None):
    if success:
        log("🟢 Health check passed.")
    else:
        log(f"🔴 Health check failed: {error}")
        send_admin_alert(
            title="🚨 EmeraldAlert Health Check Failed",
            message=f"Scan failed with error:\n\n{error}",
            level="error"
        )
