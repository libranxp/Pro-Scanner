import sys
import os
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fetch.fetch_crypto_data import fetch_crypto_data
from dispatch.dispatch_telegram import send_telegram_message
from dispatch.dispatch_discord import send_discord
from dispatch.alert_formatter import format_alert
from utils.scoring import score_crypto_alert

def scan_crypto(crypto_symbols: list):
    for symbol in crypto_symbols:
        try:
            data = fetch_crypto_data(symbol)
            alert = score_crypto_alert(symbol, data)

            if alert.get("confidence", 0) >= 70:
                formatted = format_alert(alert)
                send_telegram_message(formatted)        # ✅ Removed second argument
                send_discord(formatted, "crypto")
        except Exception as e:
            send_telegram_message(f"[CRYPTO SCAN ERROR] {symbol}: {e}")  # ✅ Fixed call
