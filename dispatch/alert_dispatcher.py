import os
import requests
from utils.logger import log
from utils.enrich import enrich_alert_data

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")
DISCORD_WEBHOOK = os.getenv("DISCORD_CRYPTO_WEBHOOK")

def format_alert(alert):
    asset_type = alert.get("type", "Crypto")
    symbol = alert.get("symbol", "N/A")
    price = alert.get("price", "N/A")
    entry = alert.get("entry", "N/A")
    stop = alert.get("stop", "N/A")
    targets = alert.get("targets", [])
    vol_spike = alert.get("vol_spike", "N/A")
    rsi = alert.get("rsi", "N/A")
    macd = alert.get("macd", "N/A")
    ema_stack = alert.get("ema_stack", "N/A")
    vwap_reclaim = alert.get("vwap_reclaim", "N/A")
    order_book_wall = alert.get("order_book_wall", "N/A")
    correlation = alert.get("btc_correlation", "N/A")
    exchanges = ", ".join(alert.get("exchanges", []))
    sentiment_surge = alert.get("sentiment_surge", "N/A")
    catalyst = alert.get("catalyst", "N/A")
    sentiment_analysis = alert.get("sentiment_analysis", "N/A")
    risk_level = alert.get("risk_level", "N/A")
    confidence = alert.get("confidence", "N/A")
    chart_link = alert.get("chart_link", "#")
    catalyst_link = alert.get("catalyst_link", "#")
    timestamp = alert.get("timestamp", "N/A")

    if asset_type.lower() == "stock":
        header = f"🚨 SCALP ALERT — {symbol} — US Stock"
    else:
        header = f"🚨 SCALP ALERT — {symbol} (Crypto USD Pair)"

    body = (
        f"{header}\n"
        f"💲 Price: {price}\n"
        f"📍 Entry: {entry} | Stop: {stop}\n"
        f"🎯 Targets: T1 {targets[0]} | T2 {targets[1]}\n"
        f"📊 Vol Spike: {vol_spike} | RSI: {rsi} | MACD: {macd}\n"
        f"📈 EMA Stack: {ema_stack} | VWAP Reclaim: {vwap_reclaim}\n"
        f"🛡️ Order Book Wall: {order_book_wall}\n"
        f"⚡ BTC Correlation: {correlation} | 🏦 Exchange: {exchanges}\n"
        f"🔥 Sentiment Surge: {sentiment_surge}\n"
        f"📰 Catalyst: {catalyst}\n"
        f"💬 Sentiment Analysis: {sentiment_analysis}\n"
        f"🛡️ Risk Level: {risk_level} | ⚡ Confidence: {confidence}%\n"
        f"📈 Chart: [TradingView]({chart_link})\n"
        f"📰 Catalyst Source: [Link]({catalyst_link})\n"
        f"⏱️ Timestamp: {timestamp}"
    )

    return body

def send_telegram_alert(alert):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHANNEL_ID:
        log("❌ Telegram credentials missing.")
        return

    message = format_alert(alert)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    response = requests.post(url, json=payload)
    log(f"📤 Telegram status: {response.status_code}")
    log(f"📤 Telegram response: {response.text}")

def send_discord_alert(alert):
    if not DISCORD_WEBHOOK:
        log("❌ Discord webhook missing.")
        return

    message = format_alert(alert)
    payload = {"content": message}

    response = requests.post(DISCORD_WEBHOOK, json=payload)
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
