def generate_reasoning(a):
    reasons = []
    if a.get("rsi", 0) > 70:
        reasons.append("Strong RSI indicates bullish momentum.")
    if a.get("macd", "") == "bullish":
        reasons.append("MACD crossover confirms trend shift.")
    if a.get("volume_spike", 0) > 2:
        reasons.append("Unusual volume confirms interest.")
    if a.get("catalyst"):
        reasons.append(f"Catalyst: {a['catalyst']}")
    if a.get("buzz_score", 0) > 70:
        reasons.append("Buzz score indicates social momentum.")
    return " ".join(reasons)

