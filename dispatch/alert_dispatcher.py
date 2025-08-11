import os
import requests
from zoneinfo import ZoneInfo
from datetime import datetime

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNELS = {
    "crypto": os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID"),
    "stock": os.getenv("TELEGRAM_STOCK_CHANNEL_ID"),
}

# Discord
DISCORD_WEBHOOKS = {
    "crypto": os.getenv("DISCORD_CRYPTO_WEBHOOK"),
    "stock": os.getenv("DISCORD_STOCK_WEBHOOK"),
}

REQUIRED_KEYS = [
    "ticker", "asset_type", "price", "entry", "stop", "target1", "target2",
    "vol_spike", "rsi", "macd", "ema_stack", "vwap_reclaim", "orderbook_wall",
    "orderbook_exchange", "btc_correlation", "exchange", "sentiment_surge",
    "catalyst", "sentiment_analysis", "risk_level", "confidence",
    "chart_link", "catalyst_link", "catalyst_link_text", "sentiment_link",
    "timestamp", "type"
]

def format_alert(alert):
    return (
        f"🚨 SCALP ALERT — {alert['ticker']} ({alert['asset_type']})\n\n"
        f"💲 Price: ${alert['price']}\n"
        f"📍 Entry: ${alert['entry']} | Stop: ${alert['stop']}\n"
        f"🎯 Targets: T1 ${alert['target1']} | T2 ${alert['target2']}\n"
        f"📊 Vol Spike: {alert['vol_spike']} | RSI: {alert['rsi']} | MACD: {alert['macd']}\n"
        f"📈 EMA Stack: {alert['ema_stack']} | VWAP Reclaim: {alert['vwap_reclaim']}\n"
        f"🛡️ Order Book Wall: {alert['orderbook_wall']} ({alert['orderbook_exchange']})\n"
        f"⚡ BTC Correlation: {alert['btc_correlation']} | 🏦 Exchange: {alert['exchange']}\n"
        f"🔥 Sentiment Surge: {alert['sentiment_surge']}\n"
        f"📰 Catalyst: {alert['catalyst']}\n"
        f"💬 Sentiment Analysis: {alert['sentiment_analysis']}\n"
        f"🛡️ Risk Level: {alert['risk_level']} | ⚡ Confidence: {alert['confidence']}%\n"
        f"📈 Chart: [TradingView]({alert['chart_link']})\n"
        f"📰 Catalyst Source: [{alert['catalyst_link_text']}]({alert['catalyst_link']})\n"
        f"💬 Sentiment Source: [LunarCrush]({alert['sentiment_link']})\n"
        f"⏱️ Timestamp: {alert['timestamp']} BST"
    )

def send_telegram_alert(message, alert_type):
    chat_id = TELEGRAM_CHANNELS.get(alert_type)
    if not TELEGRAM_BOT_TOKEN or not chat_id:
        print(f"[TELEGRAM] Missing bot token or channel ID for {alert_type}")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    response = requests.post(url, json=payload)
    print(f"[TELEGRAM] {alert_type} → {response.status_code}")

def send_discord_alert(message, alert_type):
    webhook = DISCORD_WEBHOOKS.get(alert_type)
    if not webhook:
        print(f"[DISCORD] Missing webhook for {alert_type}")
        return

    payload = {"content": message}
    response = requests.post(webhook, json=payload)
    print(f"[DISCORD] {alert_type} → {response.status_code}")

def dispatch_alert(alert):
    missing_keys = [key for key in REQUIRED_KEYS if key not in alert]
    if missing_keys:
        print(f"[ERROR] Alert missing keys: {missing_keys}")
        return

    alert_type = alert["type"]
    message = format_alert(alert)

    send_telegram_alert(message, alert_type)
    send_discord_alert(message, alert_type)
