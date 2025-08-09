from dispatch.telegram_dispatcher import send_telegram_alert
from utils.logger import log

def notify_failure(message, error):
    log(f"🚨 ALERT FAILURE: {message} — {error}")
    alert = {
        "ticker": "SYSTEM",
        "type": "dev",
        "price": "N/A",
        "entry": "N/A",
        "stop": "N/A",
        "target1": "N/A",
        "target2": "N/A",
        "volume_spike": "N/A",
        "rsi": "N/A",
        "macd": "N/A",
        "ema_stack": "N/A",
        "vwap_signal": "N/A",
        "orderbook_wall": "N/A",
        "btc_correlation": "N/A",
        "exchange": "N/A",
        "sentiment_surge": "N/A",
        "catalyst": message,
        "sentiment_analysis": str(error),
        "risk": "🔴 High",
        "confidence": 0,
        "chart_link": "https://example.com",
        "catalyst_link": "https://example.com"
    }
    try:
        send_telegram_alert(alert)
    except Exception as e:
        log(f"❌ Failed to send failure notification: {e}")
