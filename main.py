# main.py

from scanner import scan_markets
from alert_dispatcher import dispatch_alerts
from utils.logger import log
from utils.health import report_health
from utils.locks import acquire_lock, release_lock

def main():
    log("🚀 EmeraldAlert scan started.")

    # Concurrency lock to prevent overlapping runs
    if not acquire_lock("scan_lock"):
        log("⚠️ Scan already in progress. Exiting.")
        return

    try:
        # Run the market scanner to collect alerts
        alerts = scan_markets()

        # Dispatch alerts to all configured channels
        dispatch_alerts(alerts)

        # Report health status for monitoring
        report_health(success=True)

        log("✅ EmeraldAlert scan complete.")

    except Exception as e:
        log(f"❌ Scan failed: {e}")
        report_health(success=False, error=str(e))

    finally:
        release_lock("scan_lock")

if __name__ == "__main__":
    main()
