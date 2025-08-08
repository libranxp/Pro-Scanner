# scan/stock_spi.py
from fetch.fetch_stock_data import get_stock_candidates
from core.ai_validation import generate_ai_reason
from alerts.alert_formatter import format_alert
from alerts.telegram import send_telegram_alert
from alerts.discord import send_discord_alert
from core.session_filter import is_market_open

def run_stock_scan():
    if not is_market_open("stock"):
        return

    candidates = get_stock_candidates()
    for asset in candidates:
        if asset["confidence"] >= 70:
            reason = generate_ai_reason(asset["ticker"], asset)
            alert = format_alert(asset, reason)
            send_telegram_alert(alert, channel="stock")
            send_discord_alert(alert, channel="stock")
