# validator.py
import json
import os
from datetime import datetime, timedelta
from utils.logger import log

SCAN_HISTORY_FILE = "logs/scan_history.json"

def load_scan_history():
    if not os.path.exists(SCAN_HISTORY_FILE):
        return {}
    try:
        with open(SCAN_HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_scan_history(history):
    os.makedirs("logs", exist_ok=True)
    with open(SCAN_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def validate_alerts(alerts):
    history = load_scan_history()
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=60)  # Avoid duplicates within 1 hour

    validated = []
    updated_history = {}

    for alert in alerts:
        ticker = alert.get("ticker")
        if not ticker:
            continue

        last_seen = history.get(ticker)
        if last_seen:
            last_time = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%SZ")
            if last_time > cutoff:
                log(f"⏳ Skipping {ticker} — recently alerted at {last_seen}")
                continue

        validated.append(alert)
        updated_history[ticker] = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    save_scan_history(updated_history)
    return validated
