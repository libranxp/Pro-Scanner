# apis/finnhub.py
import requests, os

def get_quote(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={os.environ['FINNHUB_KEY']}"
    return requests.get(url).json()
