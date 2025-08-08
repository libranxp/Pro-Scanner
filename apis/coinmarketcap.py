# apis/coinmarketcap.py
import requests, os

def get_cmc_listings(limit=100):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": os.environ["CMC_KEY"]}
    params = {"limit": limit, "convert": "USD"}
    return requests.get(url, headers=headers, params=params).json()
