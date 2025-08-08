# apis/coinglass.py
import requests, os

def get_order_book(symbol):
    url = f"https://open-api.coinglass.com/public/v2/open_interest?symbol={symbol}"
    headers = {"coinglassSecret": os.environ["COINGLASS_KEY"]}
    return requests.get(url, headers=headers).json()
