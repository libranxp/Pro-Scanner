# utils/logger.py

from datetime import datetime
from zoneinfo import ZoneInfo

def log(message: str):
    bst_time = datetime.now(ZoneInfo("Europe/London")).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{bst_time} BST] {message}")
