import os
import requests

def fetch_stock_data(symbol: str):
    fmp_key = os.getenv("FMP_KEY")
    finnhub_key = os.getenv("FINNHUB_KEY")
    alphavantage_key = os.getenv("ALPHAVANTAGE_KEY")

    responses = {}

    # FMP Quote
    fmp_url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={fmp_key}"
    responses["fmp"] = requests.get(fmp_url).json()

    # Finnhub Quote
    finnhub_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={finnhub_key}"
    responses["finnhub"] = requests.get(finnhub_url).json()

    # AlphaVantage Overview
    alpha_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={alphavantage_key}"
    responses["alphavantage"] = requests.get(alpha_url).json()

    return responses
