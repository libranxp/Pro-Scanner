# core/session_filter.py
from datetime import datetime
from zoneinfo import ZoneInfo

BST = ZoneInfo("Europe/London")

def is_within_scan_window():
    now = datetime.now(tz=BST)
    return 8 <= now.hour < 22
