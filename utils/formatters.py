def format_telegram(alert):
    return (
        f"*🚨 SCALP ALERT — {alert['ticker']} ({alert['asset_type']})*\n\n"
        f"💲 Price: {alert['price']}\n"
        f"📍 Entry: {alert['entry']} | Stop: {alert['stop']}\n"
        f"🎯 Targets: T1 {alert['target1']} | T2 {alert['target2']}\n\n"
        f"📊 Vol Spike: {alert['vol_spike']} | RSI: {alert['rsi']} | MACD: {alert['macd']}\n"
        f"📈 EMA Stack: {alert['ema_stack']} | VWAP Reclaim: {alert['vwap_reclaim']}\n"
        f"🛡️ Order Book Wall: {alert['orderbook_wall']} ({alert['orderbook_exchange']})\n"
        f"⚡ BTC Correlation: {alert['btc_correlation']} | 🏦 Exchange: {alert['exchange']}\n\n"
        f"🔥 Sentiment Surge: {alert['sentiment_surge']}\n"
        f"📰 Catalyst: {alert['catalyst']}\n"
        f"💬 Sentiment Analysis: {alert['sentiment_analysis']}\n\n"
        f"🛡️ Risk Level: {alert['risk_level']} | ⚡ Confidence: {alert['confidence']}%\n"
        f"📈 Chart: [TradingView]({alert['chart_link']})\n"
        f"📰 Catalyst Source: [{alert['catalyst_link_text']}]({alert['catalyst_link']})\n"
        f"⏱️ Timestamp: {alert['timestamp']} UTC"
    )

def format_discord(alert):
    return (
        f"🚨 **SCALP ALERT — {alert['ticker']} ({alert['asset_type']})**\n\n"
        f"💲 Price: {alert['price']} | Entry: {alert['entry']} | Stop: {alert['stop']}\n"
        f"🎯 Targets: T1 {alert['target1']} | T2 {alert['target2']}\n\n"
        f"📊 Vol Spike: {alert['vol_spike']} | RSI: {alert['rsi']} | MACD: {alert['macd']}\n"
        f"📈 EMA Stack: {alert['ema_stack']} | VWAP Reclaim: {alert['vwap_reclaim']}\n"
        f"🛡️ Order Book Wall: {alert['orderbook_wall']} ({alert['orderbook_exchange']})\n"
        f"⚡ BTC Correlation: {alert['btc_correlation']} | 🏦 Exchange: {alert['exchange']}\n\n"
        f"🔥 Sentiment Surge: {alert['sentiment_surge']}\n"
        f"📰 Catalyst: {alert['catalyst']}\n"
        f"💬 Sentiment Analysis: {alert['sentiment_analysis']}\n\n"
        f"🛡️ Risk Level: {alert['risk_level']} | ⚡ Confidence: {alert['confidence']}%\n"
        f"📈 Chart: {alert['chart_link']}\n"
        f"📰 Catalyst Source: {alert['catalyst_link']}\n"
        f"⏱️ Timestamp: {alert['timestamp']} UTC"
    )
