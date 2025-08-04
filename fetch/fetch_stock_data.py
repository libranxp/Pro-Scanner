import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import ta
from zoneinfo import ZoneInfo

# API Keys from GitHub Secrets
FINNHUB_KEY = os.getenv('FINNHUB_KEY')
FMP_KEY = os.getenv('FMP_KEY')

BST = ZoneInfo("Europe/London")  # BST timezone reference

def fetch_ohlcv_finnhub(ticker):
    """
    Fetch intraday OHLCV data from Finnhub.
    """
    now = int(datetime.utcnow().timestamp())
    start = int((datetime.utcnow() - timedelta(days=5)).timestamp())
    url = (
        f"https://finnhub.io/api/v1/stock/candle"
        f"?symbol={ticker}&resolution=5&from={start}&to={now}&token={FINNHUB_KEY}"
    )
    res = requests.get(url)
    data = res.json()

    if data.get("s") != "ok":
        print(f"[Finnhub] No candle data for {ticker}")
        return None

    df = pd.DataFrame({
        "timestamp": pd.to_datetime(data["t"], unit="s").tz_localize("UTC").tz_convert(BST),
        "open": data["o"],
        "high": data["h"],
        "low": data["l"],
        "close": data["c"],
        "volume": data["v"]
    })

    return df


def calculate_indicators(df):
    """
    Compute RSI, EMA(5/8/13), VWAP from OHLCV.
    """
    try:
        indicators = {
            "rsi": ta.momentum.RSIIndicator(close=df["close"]).rsi().iloc[-1],
            "ema_5": ta.trend.EMAIndicator(close=df["close"], window=5).ema_indicator().iloc[-1],
            "ema_8": ta.trend.EMAIndicator(close=df["close"], window=8).ema_indicator().iloc[-1],
            "ema_13": ta.trend.EMAIndicator(close=df["close"], window=13).ema_indicator().iloc[-1],
            "vwap": ta.volume.VolumeWeightedAveragePrice(
                high=df["high"], low=df["low"], close=df["close"], volume=df["volume"]
            ).vwap().iloc[-1]
        }
        return indicators
    except Exception as e:
        print(f"[Indicators] Error: {e}")
        return None


def fetch_fundamentals_fmp(ticker):
    """
    Float, average volume, and relative volume via FMP.
    """
    try:
        profile = requests.get(
            f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={FMP_KEY}"
        ).json()

        candles = requests.get(
            f"https://financialmodelingprep.com/api/v3/historical-chart/1min/{ticker}?apikey={FMP_KEY}"
        ).json()

        stock_float = float(profile[0].get("float", 0))
        volumes = [c.get("volume", 0) for c in candles[:100]]
        avg_volume = sum(volumes) / len(volumes) if volumes else 0
        live_volume = volumes[0] if volumes else 0
        rel_volume = live_volume / avg_volume if avg_volume else 0

        return {
            "float": stock_float,
            "avg_volume": avg_volume,
            "live_volume": live_volume,
            "rel_volume": round(rel_volume, 2)
        }

    except Exception as e:
        print(f"[FMP] Error: {e}")
        return {
            "float": 0,
            "avg_volume": 0,
            "live_volume": 0,
            "rel_volume": 0
        }


def fetch_stock_data(ticker):
    """
    Final scanner payload with BST timestamp.
    """
    df = fetch_ohlcv_finnhub(ticker)
    if df is None or df.empty:
        return None

    indicators = calculate_indicators(df)
    fundamentals = fetch_fundamentals_fmp(ticker)

    return {
        "symbol": ticker,
        "asset_type": "stock",
        "price": df["close"].iloc[-1],
        "rsi": round(indicators["rsi"], 2),
        "ema_stack": {
            "ema_5": round(indicators["ema_5"], 2),
            "ema_8": round(indicators["ema_8"], 2),
            "ema_13": round(indicators["ema_13"], 2)
        },
        "vwap": round(indicators["vwap"], 2),
        "float": fundamentals["float"],
        "avg_volume": fundamentals["avg_volume"],
        "live_volume": fundamentals["live_volume"],
        "rel_volume": fundamentals["rel_volume"],
        "timestamp": datetime.now(tz=BST).strftime("%Y-%m-%d %H:%M:%S %Z")
    }
