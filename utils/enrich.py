from utils.api_wrappers import (
    get_fmp_data,
    get_crypto_data,
    get_finnhub_indicators,
    get_lunarcrush_data,
    get_messari_news,
    get_orderbook_data,
    get_santiment_correlation,
    get_orderflow_data
)

def enrich_ticker(ticker, asset_type, config):
    is_crypto = asset_type == "crypto"

    # 🔹 Fetch base data
    base = get_crypto_data(ticker) if is_crypto else get_fmp_data(ticker)
    indicators = get_finnhub_indicators(ticker) if not is_crypto else {}
    sentiment = get_lunarcrush_data(ticker) if is_crypto else {}
    news = get_messari_news(ticker) if is_crypto else {}
    orderbook = get_orderbook_data(ticker) if is_crypto else {}
    correlation = get_santiment_correlation(ticker) if is_crypto else {}
    orderflow = get_orderflow_data(ticker)

    # ✅ Defensive fallback logic
    price = base.get("price", 0)
    entry = round(price * 1.01, 2)
    stop = round(price * 0.97, 2)
    target = round(price * 1.08, 2)

    enriched = {
        "ticker": ticker,
        "asset_type": asset_type,
        "entry": entry,
        "stop": stop,
        "target": target,
        "score": config.get("score", 85),
        "volatility": base.get("atr", 0.02),
        "rvol": base.get("rvol", 1.0),
        "resistance_gap": base.get("resistance_gap", 5.0),
        "atr_spike": base.get("atr_spike", 1.0),
        "rsi": indicators.get("rsi", 50),
        "macd_histogram": indicators.get("macd_histogram", 0.5),
        "ema_stack": indicators.get("ema_stack", False),
        "sentiment_summary": sentiment.get("summary", "Neutral"),
        "galaxy_score": sentiment.get("galaxyScore", 50),
        "news_title": news.get("title", "No headline"),
        "news_url": news.get("url", ""),
        "dark_pool": orderflow.get("dark_pool", 0),
        "whale_buy": base.get("whale_buy", 0),
        "source_url": sentiment.get("url", ""),
        "channel": config.get("channel", "telegram")
    }

    return enriched
