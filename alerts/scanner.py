# alerts/scanner.py

from utils.logger import log

def scan_markets():
    """
    Scans markets and returns a list of alerts.
    Replace this stub with actual scanning logic.
    """
    log("🔍 Scanning markets...")

    alerts = [
        {
            "ticker": "ETH/USD",
            "type": "breakout",
            "message": "ETH broke above $2,000",
            "priority": "high"
        },
        {
            "ticker": "TSLA",
            "type": "gap up",
            "message": "TSLA opened 5% above previous close",
            "priority": "medium"
        }
    ]

    log(f"✅ Scan complete. Found {len(alerts)} alerts.")
    return alerts
