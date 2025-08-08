# alerts/telegram.py
import requests
import os
from utils.logger import log

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

CHANNEL_IDS = {
    "crypto": os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID"),
    "stock": os.getenv("TELEGRAM_STOCK_CHANNEL_ID"),
    "admin": os.getenv("TELEGRAM_ADMIN_CHANNEL_ID"),
    "dev": os.getenv("TELEGRAM_DEV_CHANNEL_ID"),
}

def send_telegram_alert(message, asset_type):
    chat_id = CHANNEL_IDS.get(asset_type, CHANNEL_IDS["admin"])
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    res = requests.post(f"{BASE_URL}/sendMessage", json=payload)
    if res.status_code != 200:
        raise Exception(f"Telegram error: {res.text}")

def send_admin_message(message):
    payload = {
        "chat_id": CHANNEL_IDS["admin"],
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(f"{BASE_URL}/sendMessage", json=payload)

def check_for_commands():
    offset_file = "logs/telegram_offset.txt"
    try:
        with open(offset_file, "r") as f:
            offset = int(f.read().strip())
    except:
        offset = 0

    res = requests.get(f"{BASE_URL}/getUpdates", params={"offset": offset + 1}).json()
    updates = res.get("result", [])

    if not updates:
        return None

    for update in updates:
        offset = update["update_id"]
        message = update.get("message", {})
        text = message.get("text", "").strip().lower()
        chat_id = str(message.get("chat", {}).get("id"))

        if chat_id != CHANNEL_IDS["admin"]:
            continue

        if text == "/scan now":
            log("📲 Manual scan triggered via Telegram")
            with open(offset_file, "w") as f:
                f.write(str(offset))
            return "scan"

        elif text == "/status":
            send_admin_message("✅ EmeraldAlert is online and listening.")
            with open(offset_file, "w") as f:
                f.write(str(offset))
            return None

        elif text == "/debug":
            send_admin_message("🧪 Debug mode enabled. Running dry scan...")
            with open(offset_file, "w") as f:
                f.write(str(offset))
            return "dry"

    with open(offset_file, "w") as f:
        f.write(str(offset))

    return None
