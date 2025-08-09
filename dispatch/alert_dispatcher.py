# dispatch/alert_dispatcher.py

import os
import requests
from utils.logger import log
from utils.enrich import enrich_alert_data

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CRYPTO_CHANNEL_ID = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")
DISCORD_CRYPTO_WEBHOOK = os.getenv("DISCORD_CRYPTO_WEBHOOK")

def format_alert(alert):
    return (
        f"🚨 SCALP ALERT — {alert['ticker']} ({alert['asset_type']})\n\n"
        f"💲 Price: {alert['price']}\n"
        f"📍 Entry: {alert['entry']} | Stop: {alert['stop']}\n"
        f"🎯 Targets: T1 {alert['target1']} | T2 {alert['target2']}\n"
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
        f"⏱️ Timestamp: {alert['timestamp']} UTC"
    )

def send_telegram_alert(alert):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CRYPTO_CHANNEL_ID:
        log("❌ Telegram credentials missing.")
        return

    message = format_alert(alert)
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CRYPTO_CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    response = requests.post(url, json=payload)
    log(f"📤 Telegram status: {response.status_code}")
    log(f"📤 Telegram response: {response.text}")

def send_discord_alert(alert):
    if not DISCORD_CRYPTO_WEBHOOK:
        log("❌ Discord webhook missing.")
        return

    message = format_alert(alert)
    payload = {"content": message}

    response = requests.post(DISCORD_CRYPTO_WEBHOOK, json=payload)
    log(f"📤 Discord status: {response.status_code}")
    log(f"📤 Discord response: {response.text}")

def dispatch_alerts(alerts):
    if not alerts:
        log("ℹ️ No alerts to dispatch.")
        return

    log(f"📊 Dispatching {len(alerts)} alerts...")

    for raw_alert in alerts:
        enriched = enrich_alert_data(raw_alert)
        send_telegram_alert(enriched)
        send_discord_alert(enriched)
