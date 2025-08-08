from telegram_dispatcher import send_telegram_message

if __name__ == "__main__":
    try:
        send_telegram_message("debug", "✅ Telegram dispatch test successful.")
        print("Message sent.")
    except Exception as e:
        print(f"Dispatch failed: {e}")
