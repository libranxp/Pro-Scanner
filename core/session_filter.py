# core/session_filter.py
def is_market_open(asset_type):
    from datetime import datetime
    now = datetime.utcnow()
    if asset_type == "stock":
        return now.weekday() < 5 and 13 <= now.hour <= 20  # 08:00–15:00 EST
    elif asset_type == "crypto":
        return True
    return False
