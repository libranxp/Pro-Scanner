# utils/logger.py
import datetime

def log(message):
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"[{timestamp}] {message}")
