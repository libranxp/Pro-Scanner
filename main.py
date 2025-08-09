# main.py

from core.scanner import scan_markets
from dispatch.alert_dispatcher import dispatch_alerts
from utils.logger import log
from utils.health import report_health
from utils.locks import acquire_lock, release_lock

def main():
    log("🚀 EmeraldAlert scan started.")

    if not acquire_lock("scan_lock"):
        log("⚠️ Scan already in progress. Exiting.")
        return

    try:
        alerts = scan_markets()
        log(f"📊 Total alerts found: {len(alerts)}")
        dispatch_alerts(alerts)
        report_health(success=True)
        log("✅ EmeraldAlert scan complete.")
    except Exception as e:
        log(f"❌ Scan failed: {e}")
        report_health(success=False, error=str(e))
    finally:
        release_lock("scan_lock")

if __name__ == "__main__":
    main()
