# formatter.py
def format_alert(alert):
    ticker = alert.get("ticker", "N/A")
    price = alert.get("price", "N/A")
    change = alert.get("change_percent", "N/A")
    volume = alert.get("volume", "N/A")
    confidence = alert.get("confidence", "N/A")
    strategy = alert.get("strategy", "Unknown")

    lines = [
        f"📈 **{ticker} Alert**",
        f"💰 Price: ${price}",
        f"📊 Change: {change}%",
        f"🔄 Volume: {volume}",
        f"🧠 Confidence: {confidence}",
        f"🧪 Strategy: `{strategy}`",
    ]

    return "\n".join(lines)

def format_admin_notice(message, level="info"):
    emoji = {
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "❌",
        "success": "✅"
    }.get(level, "ℹ️")

    return f"{emoji} **Admin Notice**\n{message}"
