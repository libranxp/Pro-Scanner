# core/execution_plan.py
from datetime import datetime

def should_run_scan():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    return (8 <= hour <= 22) and (minute % 30 == 0)
