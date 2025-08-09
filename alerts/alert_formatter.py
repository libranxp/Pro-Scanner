# alerts/alert_formatter.py

from datetime import datetime

def format_telegram(data):
    return f"""
🚨 *SCALP ALERT — {data['ticker']} ({data['asset_type']})*

💲 *Price:* {data['price']}
📍 *Entry:* {data['entry']} | *Stop:* {data['stop']}
🎯 *Targets:* T1 {data['target1']} | T2 {data['target2']}

📊 *Vol Spike:* {data['volume_spike']} | *RSI:* {data['rsi']} | *MACD:* {data['macd']}
📈 *EMA Stack:* {data['ema_stack']} | *VWAP Reclaim:* {data['vwap_signal']}
🛡️ *Order Book Wall:* {data['orderbook_wall']}
⚡ *BTC Correlation:* {data['btc_correlation']} | 🏦 *Exchange:* {data['exchange']}

🔥 *Sentiment Surge:* {data['sentiment_surge']}
📰 *Catalyst:* {data['catalyst']}
💬 *Sentiment Analysis:* {data['sentiment_analysis']}

🛡️ *Risk Level:* {data['risk']} | ⚡ *Confidence:* {data['confidence']}%
📈 [Chart]({data['chart_link']})
📰 [Catalyst Source]({data['catalyst_link']})
⏱️ *Timestamp:* {data['timestamp']}
""".strip()

def format_discord(data):
    return {
        "username": "EmeraldAlert",
        "embeds": [
            {
                "title": f"🚨 SCALP ALERT — {data['ticker']} ({data['asset_type']})",
                "color": get_color(data['risk']),
                "fields": [
                    {"name": "Price", "value": data['price'], "inline": True},
                    {"name": "Entry / Stop", "value": f"{data['entry']} / {data['stop']}", "inline": True},
                    {"name": "Targets", "value": f"T1: {data['target1']} | T2: {data['target2']}", "inline": True},
                    {"name": "Volume Spike", "value": data['volume_spike'], "inline": True},
                    {"name": "RSI / MACD", "value": f"{data['rsi']} / {data['macd']}", "inline": True},
                    {"name": "VWAP / EMA", "value": f"{data['vwap_signal']} / {data['ema_stack']}", "inline": True},
                    {"name": "Order Book Wall", "value": data['orderbook_wall'], "inline": True},
                    {"name": "Exchange", "value": data['exchange'], "inline": True},
                    {"name": "Sentiment", "value": f"{data['sentiment_surge']} — {data['sentiment_analysis']}", "inline": False},
                    {"name": "Catalyst", "value": data['catalyst'], "inline": False},
                    {"name": "Confidence", "value": f"{data['confidence']}%", "inline": True},
                    {"name": "Risk Level", "value": data['risk'], "inline": True},
                    {"name": "Timestamp", "value": data['timestamp'], "inline": False}
                ],
                "footer": {"text": "EmeraldAlert"},
                "url": data['chart_link']
            }
        ]
    }

def get_color(risk):
    if "🔴" in risk or "High" in risk:
        return 0xFF0000
    elif "🟡" in risk or "Medium" in risk:
        return 0xFFFF00
    elif "🟢" in risk or "Low" in risk:
        return 0x00FF00
    return 0xCCCCCC

def enrich_alert_data(data):
    data['timestamp'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    return data
