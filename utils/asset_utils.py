def format_price(p):
    return f"£{round(p, 4)}"

def normalize_symbol(symbol):
    return symbol.upper().replace("USDT", "").replace("USD", "")

def get_emoji_by_score(score):
    return "🟩" if score >= 80 else "🟨" if score >= 60 else "🟥"

