import requests

def fetch_top_crypto_gainers():
    url = "https://api.dexscreener.com/latest/dex/pairs"
    res = requests.get(url).json()
    return [p for p in res.get("pairs", []) if float(p.get("priceChange", 0)) > 3]

def fetch_top_stock_gainers():
    url = "https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey=YOUR_KEY"
    res = requests.get(url).json()
    return [s for s in res if float(s.get("changesPercentage", 0)) > 3]

