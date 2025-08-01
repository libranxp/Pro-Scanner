import os
import requests

def fetch_sentiment_and_catalyst(symbol: str):
    santiment_key = os.getenv("SANTIMENT_KEY")
    
    # Santiment social sentiment
    sentiment_url = f"https://api.santiment.net/news/v1/sentiment?tickers={symbol}&apikey={santiment_key}"
    sentiment = requests.get(sentiment_url).json()

    return {"santiment": sentiment}
