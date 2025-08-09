import os
import requests
from apis.messari import fetch_asset_metrics
from apis.santiment import fetch_social_volume
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
                        "type": "crypto",
                        "source": "coinmarketcap"
                    })
        except Exception as e:
            log(f"❌ CMC fetch failed: {e}")
    else:
        log("⚠️ Missing CMC_KEY")

    # --- Stocks: FMP ---
    fmp_key = os.getenv("FMP_KEY")
    if fmp_key:
        try:
            url = f"https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=100000000&volumeMoreThan=500000&priceMoreThan=5&apikey={fmp_key}"
            res = requests.get(url)
            data = res.json()
            for stock in data[:100]:
                symbol = stock.get("symbol")
                price = stock.get("price")
                change = stock.get("changesPercentage")
                volume = stock.get("volume")
                market_cap = stock.get("marketCap")

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
                        "type": "stocks",
                        "source": "fmp"
                    })
        except Exception as e:
            log(f"❌ FMP fetch failed: {e}")
    else:
        log("⚠️ Missing FMP_KEY")

    # --- Crypto: Messari (Bitcoin) ---
    messari_key = os.getenv("MESSARI_API_KEY")
    if messari_key:
        try:
            btc_metrics = fetch_asset_metrics("bitcoin", messari_key)
            change = btc_metrics["data"]["market_data"]["percent_change_usd_last_24_hours"]
            if abs(change) >= 5:
                alerts.append({
                    "ticker": "BTC",
                    "price": btc_metrics["data"]["market_data"]["price_usd"],
                    "change": round(change, 2),
                    "confidence": min(100, abs(change) * 10),
                    "type": "crypto",
                    "source": "messari"
                })
        except Exception as e:
            log(f"❌ Messari fetch failed: {e}")
    else:
        log("⚠️ Missing MESSARI_API_KEY")

    # --- Crypto: Santiment (Ethereum social volume) ---
    santiment_key = os.getenv("SANTIMENT_API_KEY")
    if santiment_key:
        try:
            eth_social = fetch_social_volume("ethereum", santiment_key)
            latest = eth_social["data"]["getMetric"]["timeseriesData"][-1]
            volume_score = latest["value"]
            if volume_score >= 100:
                alerts.append({
                    "ticker": "ETH",
                    "confidence": min(100, int(volume_score)),
                    "type": "crypto",
                    "source": "santiment"
                })
        except Exception as e:
            log(f"❌ Santiment fetch failed: {e}")
    else:
        log("⚠️ Missing SANTIMENT_API_KEY")

    return alerts
