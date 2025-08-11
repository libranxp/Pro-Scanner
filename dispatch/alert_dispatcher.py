from utils.channel_router import send_to_channel

def dispatch_alert(alert):
    ticker = alert["ticker"]
    entry = alert["entry"]
    stop = alert["stop"]
    target = alert["target"]
    channel = alert["channel"]

    message = (
        f"🚨 *{ticker} Signal*\n"
        f"Entry: ${entry:.2f}\n"
        f"Stop: ${stop:.2f}\n"
        f"Target: ${target:.2f}"
    )

    print(f"[DISPATCH] Alert for {ticker} → {channel}")
    send_to_channel(channel, message)
