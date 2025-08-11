from utils.channel_router import send_to_channel

def dispatch_alert(alert):
    ticker = alert.get("ticker", "UNKNOWN")
    channel = alert.get("channel", "telegram")  # Default to Telegram if not specified

    message = (
        f"🚨 Alert for {ticker}\n"
        f"Entry: ${alert.get('entry', 'N/A')} | "
        f"Stop: ${alert.get('stop', 'N/A')} | "
        f"Target: ${alert.get('target', 'N/A')}"
    )

    print(f"[DISPATCH] Sending alert for {ticker} to {channel}...")
    send_to_channel(channel, message)
