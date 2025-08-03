import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from validation.reasoning_builder import generate_reasoning
from dispatch.dispatch_telegram import send_telegram_message

def load_alerts():
    with open("logs/scan_history.json") as f:
        return json.load(f)

def run_validation():
    alerts = load_alerts()
    for a in alerts:
        if a.get("score", 0) >= 75:
            summary = generate_reasoning(a)
            msg = f"🧠 AI Summary — {a['symbol']}\n✅ {summary}\n🎯 TP: {a.get('target','-')} | SL: {a.get('stop','-')} | Score: {a['score']}%"
            send_telegram(msg, "admin")

if __name__ == "__main__":
    run_validation()

