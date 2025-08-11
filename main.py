from alerts.scanner import scan_stocks, scan_crypto
from utils.enrich import enrich_ticker
from dispatch.alert_dispatcher import dispatch_alert
from utils.logger import log

def run_alert_engine():
    log("🚀 Starting EmeraldAlert engine...")

    stock_candidates = scan_stocks()
    crypto_candidates = scan_crypto()

    all_alerts = []

    for ticker in stock_candidates:
        enriched = enrich_ticker(ticker, "stock", {"type": "stock"})
        all_alerts.append(enriched)

    for ticker in crypto_candidates:
        enriched = enrich_ticker(ticker, "crypto", {"type": "crypto"})
        all_alerts.append(enriched)

    for alert in all_alerts:
        dispatch_alert(alert)

    log(f"✅ Dispatched {len(all_alerts)} alerts.")

if __name__ == "__main__":
    run_alert_engine()
