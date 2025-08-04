import os
import requests

def fetch_crypto_data(symbol: str):
    key = os.getenv("LUNARCRUSH_KEY")  # ✅ matches GitHub secret name
    lunar_url = f"https://api.lunarcrush.com/v2?data=assets&key={key}&symbol={symbol}"
    headers = {"Accept": "application/json"}

    responses = {}
    try:
        response = requests.get(lunar_url, headers=headers, timeout=10)
        responses["lunar"] = response.json()
    except Exception as e:
        print(f"[LunarCrush] Error fetching data for {symbol}: {e}")
        responses["lunar"] = {}

    return responses
