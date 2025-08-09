# scanner.py
import os
import requests
from utils.logger import log

def scan_markets():
    alerts = []

    # --- Crypto: CoinMarketCap ---
    cmc_key = os.getenv("CMC_KEY")
    if cmc_key:
        try:
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
            headers = {"X-CMC_PRO_API_KEY": cmc_key}
            params = {"limit": 100, "convert": "USD"}
            res = requests.get(url, headers=headers, params=params)
            data = res.json().get("data", [])
            for coin in data:
                price = coin["quote"]["USD"]["price"]
                change = coin["quote"]["USD"]["percent_change_24h"]
                volume = coin["quote"]["USD"]["volume_24h"]
                market_cap = coin["quote"]["USD"]["market_cap"]

                # --- Scanning Criteria ---
                if (
                    abs(change) >= 5 and
                    volume >= 50_000_000 and
                    market_cap >= 100_000_000
                ):
                    alerts.append({
                        "ticker": coin["symbol"],
                        "name": coin["name"],
                        "price": round(price, 2),
                        "change": round(change, 2),
                        "volume": round(volume, 2),
                        "market_cap": round(market_cap, 2),
                        "confidence": min(100, abs(change) * 10),
                        "type": "crypto"
                    })
        except Exception as e:
            log(f"❌ CMC fetch failed: {e}")

    # --- Stocks: FMP (Financial Modeling Prep) ---
    fmp_key = os.getenv("FMP_KEY")
    if fmp_key:
        try:
            url = f"https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=100000000&volumeMoreThan=500000&priceMoreThan=5&apikey={fmp_key}"
            res = requests.get(url)
            data = res.json()
            for stock in data[:100]:  # Limit to top 100
                symbol = stock.get("symbol")
                price = stock.get("price")
                change = stock.get("changesPercentage")
                volume = stock.get("volume")
                market_cap = stock.get("marketCap")

                # --- Scanning Criteria ---
                if (
                    symbol and
                    abs(change) >= 2 and
                    volume >= 500_000 and
                    market_cap >= 100_000_000
                ):
                    alerts.append({
                        "ticker": symbol,
                        "price": round(price, 2),
                        "change": round(change, 2),
                        "volume": volume,
                        "market_cap": market_cap,
                        "confidence": min(100, abs(change) * 20),
                        "type": "stocks"
                    })
        except Exception as e:
            log(f"❌ FMP fetch failed: {e}")

    return alerts
