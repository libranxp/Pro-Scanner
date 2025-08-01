def score_equity_alert(symbol: str, raw_data: dict) -> dict:
    quote = raw_data["fmp"][0] if raw_data.get("fmp") else {}
    sentiment = raw_data.get("alphavantage", {}).get("Sector")  # placeholder

    # Example scoring logic
    confidence = 0
    tier = "N/A"
    rel_vol = quote.get("volume", 0) / quote.get("avgVolume", 1)
    rsi = raw_data.get("finnhub", {}).get("rsi", 50)

    if rel_vol > 1.5:
        confidence += 30
    if 30 < rsi < 70:
        confidence += 20

    tier = "High" if confidence >= 80 else "Medium" if confidence >= 60 else "Low"
    confidence_emoji = "✅" if confidence >= 80 else "⚠️" if confidence >= 60 else "🔍"

    return {
        "symbol": symbol,
        "strategy": "Breakout Momentum",
        "entry": quote.get("price", 0),
        "tp": quote.get("price", 0) * 1.05,
        "sl": quote.get("price", 0) * 0.95,
        "confidence": confidence,
        "tier": tier,
        "confidence_emoji": confidence_emoji,
        "sentiment": sentiment,
        "bias": "Neutral",
        "catalyst": "Earnings Preview",
        "float": quote.get("sharesOutstanding", 0) / 1_000_000,
        "rel_vol": round(rel_vol, 2),
        "rsi": rsi,
        "atr": "N/A",
        "note": "Pre-market volume surge detected"
    }
def score_crypto_alert(symbol: str, core: dict, sentiment: dict) -> dict:
    cmc = core["cmc"]["data"][symbol]
    sentiment_score = sentiment["santiment"].get("score", 50)

    confidence = 0
    tier = "N/A"

    if cmc["quote"]["USD"]["percent_change_24h"] > 5:
        confidence += 30
    if sentiment_score > 60:
        confidence += 30

    tier = "High" if confidence >= 80 else "Medium" if confidence >= 60 else "Low"
    confidence_emoji = "🚀" if confidence >= 80 else "🌥️" if confidence >= 60 else "🔍"

    return {
        "symbol": symbol,
        "strategy": "Volatility Play",
        "entry": cmc["quote"]["USD"]["price"],
        "tp": cmc["quote"]["USD"]["price"] * 1.08,
        "sl": cmc["quote"]["USD"]["price"] * 0.95,
        "confidence": confidence,
        "tier": tier,
        "confidence_emoji": confidence_emoji,
        "sentiment": sentiment_score,
        "bias": "Bullish" if sentiment_score > 60 else "Neutral",
        "catalyst": "Network Upgrade",
        "float": "N/A",
        "rel_vol": "N/A",
        "rsi": "N/A",
        "atr": "N/A",
        "note": "Spike in on-chain mentions"
    }
