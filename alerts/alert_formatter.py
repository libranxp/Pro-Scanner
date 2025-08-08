# alerts/alert_formatter.py
def format_alert(asset, reason):
    return f"""
🚨 [ALERT] — ${asset['ticker']}

📈 Price: {asset['price']} ({asset['change']}%)
📊 Volume Spike: RVOL {asset['volume']}
📍 Entry: {asset['entry']} | Stop: {asset['stop']} | Target: {asset['target']}

📌 Technicals: {asset['technicals']}
🧠 AI Reason: {reason}
📣 Catalyst: {asset['catalyst']}
📊 Sentiment: {asset['sentiment']}

📅 Timestamp: {asset['timestamp']}
🔗 [View Chart]({asset['chart_url']})
""".strip()
