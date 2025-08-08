# alerts/alert_formatter.py
def format_alert(data):
    return f"""
🚨 *{data['ticker']}* — {data['risk']} Risk

💲 *Price:* {data['price']} | *Change:* {data['change']}%
📍 *Entry:* {data['entry']} | *Stop:* {data['stop']} | *Target:* {data['target']}
📊 *Volume Spike:* {data['volume']} | *Confidence:* {data['confidence']}%
📈 *Technicals:* {data['technicals']}
📰 *Catalyst:* {data['catalyst']}
🔥 *Sentiment:* {data['sentiment']}
📅 *Timestamp:* {data['timestamp']}
🔗 [Chart]({data['chart_url']})
""".strip()
