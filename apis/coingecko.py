# apis/coingecko.py
import requests

def get_coingecko_listings():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "volume_desc", "per_page": 100}
    return requests.get(url, params=params).json()
