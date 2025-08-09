def format_telegram(alert):
    return (
        f"*🚨 Alert — {alert['ticker']}*\n"
        f"Price: `{alert['price']}`\n"
        f"Entry: `{alert['entry']}`\n"
        f"Stop: `{alert['stop']}`\n"
        f"Target: `{alert['target']}`\n"
        f"Source: `{alert['source']}`\n"
        f"Time: `{alert['timestamp']}`"
    )

def format_discord(alert):
    return (
        f"🚨 **{alert['ticker']} Alert**\n"
        f"Price: `{alert['price']}` | Entry: `{alert['entry']}` | "
        f"Stop: `{alert['stop']}` | Target: `{alert['target']}`\n"
        f"Source: `{alert['source']}` | Time: `{alert['timestamp']}`"
    )
