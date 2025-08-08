# apis/messari.py
import requests, os

def get_messari_meta(symbol):
    url = f"https://data.messari.io/api/v1/assets/{symbol}/metrics"
    headers = {"x-messari-api-key": os.environ["MESSARI_KEY"]}
    return requests.get(url, headers=headers).json()
