# utils/health.py

from utils.logger import log

def report_health(success=True, error=None):
    if success:
        log("🟢 Health check passed.")
    else:
        log(f"🔴 Health check failed: {error}")
