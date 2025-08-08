# core/scoring.py
def calculate_confidence(data):
    score = 0

    # Technical Alignment (40%)
    if "EMA stack bullish" in data["technicals"]:
        score += 20
    if "MACD crossover" in data["technicals"]:
        score += 10
    if "VWAP reclaim" in data["technicals"]:
        score += 10

    # Volume & Catalyst Strength (30%)
    if data["volume"] > 1000000:
        score += 15
    if "upgrade" in data["catalyst"].lower() or "earnings" in data["catalyst"].lower():
        score += 15

    # Sentiment Spike (20%)
    if "Bullish" in data["sentiment"]:
        score += 20

    # Exchange Liquidity (10%)
    if "Binance" in data["chart_url"] or "NASDAQ" in data["chart_url"]:
        score += 10

    return min(score, 100)
