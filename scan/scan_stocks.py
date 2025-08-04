import sys
import os
import requests

# Ensure repo root is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fetch.fetch_stock_data import fetch_stock_data
from dispatch.dispatch_telegram import send_telegram_message
from dispatch.dispatch_discord import send_discord
from dispatch.alert_formatter import format_alert
from utils.scoring import score_equity_alert

def scan_stock_assets(symbols: list):
    """
    Scans stock symbols, evaluates alert confidence, and dispatches high-confidence alerts.
    """
    for symbol in symbols:
        try:
            data = fetch_stock_data(symbol)
            alert = score_equity_alert(symbol, data)

            if alert["confidence"] >= 70:
                formatted = format_alert(alert)
                send_telegram_message(formatted, "stock")
                send_discord(formatted, "stock")
        except Exception as e:
            send_telegram_message(f"[STOCK SCAN ERROR] {symbol}: {e}", "admin")
