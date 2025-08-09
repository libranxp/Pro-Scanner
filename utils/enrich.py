from datetime import datetime

def enrich_alert_data(raw):
    return {
        "ticker": raw.get("ticker", "N/A"),
        "asset_type": raw.get("asset_type", "Crypto USD Pair" if "USD" in raw.get("ticker", "") else "US Stock"),
        "price": raw.get("price", "N/A"),
        "entry": raw.get("entry", "N/A"),
        "stop": raw.get("stop", "N/A"),
        "target1": raw.get("target1", "N/A"),
        "target2": raw.get("target2", "N/A"),
        "vol_spike": raw.get("vol_spike", "N/A"),
        "rsi": raw.get("rsi", "N/A"),
        "macd": raw.get("macd", "N/A"),
        "ema_stack": raw.get("ema_stack", "N/A"),
        "vwap_reclaim": raw.get("vwap_reclaim", "N/A"),
        "orderbook_wall": raw.get("orderbook_wall", "N/A"),
        "orderbook_exchange": raw.get("orderbook_exchange", "N/A"),
        "btc_correlation": raw.get("btc_correlation", "N/A"),
        "exchange": raw.get("exchange", "N/A"),
        "sentiment_surge": raw.get("sentiment_surge", "N/A"),
        "catalyst": raw.get("catalyst", "N/A"),
        "sentiment_analysis": raw.get("sentiment_analysis", "N/A"),
        "risk_level": raw.get("risk_level", "N/A"),
        "confidence": raw.get("confidence", "N/A"),
        "chart_link": raw.get("chart_link", "https://www.tradingview.com"),
        "catalyst_link": raw.get("catalyst_link", "https://coinmarketcap.com"),
        "catalyst_link_text": raw.get("catalyst_link_text", "Source"),
        "timestamp": raw.get("timestamp", datetime.utcnow().strftime("%Y-%m-%d %H:%M")),
        "type": raw.get("type", "crypto").lower()
    }
