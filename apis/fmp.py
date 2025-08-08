# apis/fmp.py
import requests, os

def get_screener():
    url = f"https://financialmodelingprep.com/api/v3/stock-screener?apikey={os.environ['FMP_KEY']}&volumeMoreThan=1000000&priceMoreThan=0.01&priceLowerThan=50"
    return requests.get(url).json()
