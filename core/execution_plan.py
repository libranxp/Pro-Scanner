# core/execution_plan.py
from scan.crypto_spi import scan_crypto
from scan.stock_spi import scan_stocks
from core.scoring import calculate_confidence
from core.session_filter import is_within_scan_window

def run_scan():
    if not is_within_scan_window():
        return []

    crypto_raw = scan_crypto()
    stock_raw = scan_stocks()
    all_raw = crypto_raw + stock_raw

    final_alerts = []

    for item in all_raw:
        score = calculate_confidence(item)
        if score >= 70:
            item["confidence"] = score
            final_alerts.append(item)

    return final_alerts
