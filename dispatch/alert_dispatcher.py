# dispatch/alert_dispatcher.py

import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.logger import log
from utils.enrich import enrich_alert_data

# Telegram & Discord credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADMIN_CHANNEL_ID = os.getenv("TELEGRAM_ADMIN_CHANNEL_ID")
DISCORD_ADMIN_ERRORS_WEBHOOK = os.getenv("DISCORD_ADMIN_ERRORS_WEBHOOK")
TELEGRAM_CRYPTO_CHANNEL_ID = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")
DISCORD_CRYPTO_WEBHOOK = os.getenv("DISCORD_CRYPTO_WEBHOOK")

def send_admin_alert(title: str, message: str, level: str = "info"):
    """
    Sends an admin alert to Telegram and Discord with BST timestamp.
    """
    bst_time = datetime.now(ZoneInfo("Europe/London")).strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{title}\n{message}\n\n🕒 Timestamp: {bst_time} BST"

    # Telegram
    if TELEGRAM_BOT_TOKEN and TELEGRAM_ADMIN_CHANNEL_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_ADMIN_CHANNEL_ID,
                "text": full_message,
                "parse_mode": "Markdown"
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            log("📨 Admin alert sent to Telegram.")
        except Exception as e:
            log(f"⚠️ Failed to send Telegram admin alert: {e}")

    # Discord
    if DISCORD_ADMIN_ERRORS_WEBHOOK:
        try:
            payload = {"content": full_message}
            response = requests.post(DISCORD_ADMIN_ERRORS_WEBHOOK, json=payload)
            response.raise_for_status()
            log("📨 Admin alert sent to Discord.")
        except Exception as e:
            log(f"⚠️ Failed to send Discord admin alert: {e}")

def dispatch_alerts(alerts):
    """
    Dispatches enriched alerts to Telegram and Discord.
    """
    if not alerts:
        log("ℹ️ No alerts to dispatch.")
        return

    log(f"📊 Dispatching {len(alerts)} alerts...")

    for raw_alert in alerts:
        enriched = enrich_alert_data(raw_alert)
        message = format_alert(enriched)
        send_telegram_alert(message)
        send_discord_alert(message)

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

def send_telegram_alert(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CRYPTO_CHANNEL_ID:
        log("❌ Telegram credentials missing.")
        return

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

def send_discord_alert(message: str):
    if not DISCORD_CRYPTO_WEBHOOK:
        log("❌ Discord webhook missing.")
        return

    payload = {"content": message}
    response = requests.post(DISCORD_CRYPTO_WEBHOOK, json=payload)
    log(f"📤 Discord status: {response.status_code}")
    log(f"📤 Discord response: {response.text}")
