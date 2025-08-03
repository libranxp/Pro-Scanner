import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fetch.fetch_crypto_data import fetch_crypto_data
from fetch.fetch_sentiment_catalyst import fetch_sentiment_and_catalyst
from dispatch.dispatch_telegram import send_telegram_message
from dispatch.dispatch_discord import send_discord
from dispatch.alert_formatter import format_alert
from utils.scoring import score_crypto_alert

def scan_crypto(symbols: list):
    for symbol in symbols:
        try:
            core_data = fetch_crypto_data(symbol)
            sentiment_data = fetch_sentiment_and_catalyst(symbol)

            alert = score_crypto_alert(symbol, core_data, sentiment_data)

            if alert["confidence"] >= 70:
                formatted = format_alert(alert)
                send_telegram(formatted, "crypto")
                send_discord(formatted, "crypto")
        except Exception as e:
            send_telegram(f"[CRYPTO SCAN ERROR] {symbol}: {e}", "admin")
