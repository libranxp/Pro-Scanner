import os
from utils.channel_router import send_to_channel

def dispatch_alert(alert):
    ticker = alert.get("ticker", "UNKNOWN")
    is_crypto = alert.get("asset_type", "stock") == "crypto"

    # 🧠 Format alert message
    lines = [
        f"🚨 {'Crypto' if is_crypto else 'Stock'} Alert: {ticker}",
        f"📍 Entry: ${alert['entry']} | Stop: ${alert['stop']} | Target: ${alert['target']}",
        f"📊 Score: {alert['score']} | Volatility: {alert['volatility']} | RVol: {alert['rvol']}",
        f"📈 Resistance Gap: {alert['resistance_gap']} | ATR Spike: {alert['atr_spike']}",
        f"🧠 Indicators: RSI {alert['rsi']} | MACD {alert['macd_histogram']} | EMA Stack: {alert['ema_stack']}",
        f"🗣️ Sentiment: {alert.get('sentiment_summary', 'N/A')} | Galaxy Score: {alert.get('galaxy_score', 'N/A')}",
        f"📰 News: {alert.get('news_title', 'No headline')} → {alert.get('news_url', '')}",
        f"📦 Orderflow: Dark Pool ${alert.get('dark_pool', 0)} | Whale Buy ${alert.get('whale_buy', 0)}",
        f"🔗 Source: {alert.get('source_url', 'N/A')}"
    ]

    message = "\n".join(lines)

    # 🛠️ Send to appropriate channel
    channel = alert.get("channel", "default")
    send_to_channel(channel, message)

    # ✅ Log dispatch
    print(f"[DISPATCHED] {ticker} → {channel}")
