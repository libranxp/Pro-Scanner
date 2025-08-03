def format_alert(data):
    return f"""**Symbol:** ${data['symbol']}
**Strategy:** {data['strategy']}
**Entry:** ${data['entry']} | TP: ${data['tp']} | SL: ${data['sl']}
**Confidence Score:** {data['confidence_emoji']} {data['confidence']}% ({data['tier']})
**Catalyst:** {data['catalyst']}
**Sentiment Score:** {data['sentiment']} ({data['bias']})

📊 Float: {data['float']}M | Rel Vol: {data['rel_vol']} | RSI: {data['rsi']} | ATR: {data['atr']}
🔗 [TradingView Chart](https://tradingview.com/symbols/{data['symbol']}/)
🔗 [Buy on Trading212](https://www.trading212.com/)
🔗 [Order Book](https://bookmap.com/{data['symbol'].lower()})
🔗 [Catalyst News](https://benzinga.com/news/{data['symbol']})

📝 *Analyst Note:* {data['note']}
"""

