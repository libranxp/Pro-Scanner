import os
import requests
from utils.logger import log
from utils.enrich import enrich_alert_data

# Telegram channels
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNELS = {
    "crypto": os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID"),
    "stock": os.getenv("TELEGRAM_STOCK_CHANNEL_ID"),
    "error": os.getenv("TELEGRAM_ADMIN_CHANNEL_ID"),
}

# Discord webhooks
DISCORD_WEBHOOKS = {
    "crypto": os.getenv("DISCORD_CRYPTO_WEBHOOK"),
    "stock": os.getenv("DISCORD_STOCK_WEBHOOK"),
    "error": os.getenv("DISCORD_ADMIN_ERRORS_WEBHOOK"),
}

def format_alert(alert):
    return (
        f"🚨 SCALP ALERT — {alert['ticker']} ({alert['asset_type']})\n\n"
        f"💲 Price: ${alert['price']}\n"
        f"📍 Entry: ${alert['entry']} | Stop: ${alert['stop']}\n"
        f"🎯 Targets: T1 ${alert['target1']} | T2 ${alert['target2']}\n"
        f"📊 Vol Spike: {alert['vol_spike']} | RSI: {alert['rsi']} | MACD: {alert['macd']}\n"
        f"📈 EMA Stack: {alert['ema_stack']} | VWAP Reclaim: {alert['vwap_reclaim']}\n"
        f"🛡️ Order Book Wall: {alert['orderbook_wall']} ({alert['orderbook_exchange']})\n"
        f"⚡ BTC Correlation: — | 🏦 Exchange: {alert['exchange']}\n"
        f"🔥 Sentiment Surge: {alert['sentiment_surge']}\n"
        f"📰 Catalyst: {alert['catalyst']}\n"
        f"💬 Sentiment Analysis: {alert['sentiment_analysis']}\n"
        f"🛡️ Risk Level: {alert['risk_level']} | ⚡ Confidence: {alert['confidence']}%\n"
        f"📈 Chart: [TradingView]({alert['chart_link']})\n"
        f"📰 Catalyst Source: [{alert['catalyst_link_text']}]({alert['catalyst_link']})\n"
        f"💬 Sentiment Source: [LunarCrush]({alert['sentiment_link']})\n"
        f"⏱️ Timestamp: {alert['timestamp']} UTC"
    )

def send_telegram_alert(message, alert_type):
    channel_id = TELEGRAM_CHANNELS.get(alert_type)
    if not TELEGRAM_BOT_TOKEN or not channel_id:
        log(f"❌ Telegram routing failed for type: {alert_type}")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": channel_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    requests.post(url, json=payload)

def send_discord_alert(message, alert_type):
    webhook = DISCORD_WEBHOOKS.get(alert_type)
    if not webhook:
        log(f"❌ Discord routing failed for type: {alert_type}")
        return
    requests.post(webhook, json={"content": message})

def send_admin_alert(message):
    """Send alert to admin channels for errors or health checks."""
    send_telegram_alert(message, "error")
    send_discord_alert(message, "error")

def dispatch_alerts(alerts):
    for raw in alerts:
        enriched = enrich_alert_data(raw)
        msg = format_alert(enriched)
        alert_type = enriched["type"]
        send_telegram_alert(msg, alert_type)
        send_discord_alert(msg, alert_type)
