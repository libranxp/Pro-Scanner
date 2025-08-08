# apis/alpha_vantage.py
import requests, os

def get_backup_quote(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={os.environ['ALPHAVANTAGE_KEY']}"
    return requests.get(url).json()
