from fetch.fetch_stock_data import fetch_stock_data
from dispatch.dispatch_telegram import send_telegram
from dispatch.dispatch_discord import send_discord
from dispatch.alert_formatter import format_alert
from utils.scoring import score_equity_alert

def scan_stocks(symbols: list):
    for symbol in symbols:
        try:
            data = fetch_stock_data(symbol)
            alert = score_equity_alert(symbol, data)

            if alert["confidence"] >= 70:
                formatted = format_alert(alert)
                send_telegram(formatted, "stock")
                send_discord(formatted, "stock")
        except Exception as e:
            send_telegram(f"[STOCK SCAN ERROR] {symbol}: {e}", "admin")
