from datetime import datetime
from zoneinfo import ZoneInfo
from utils.api_wrappers import (
    get_fmp_data, get_finnhub_indicators, get_lunarcrush_data,
    get_messari_news, get_santiment_correlation, get_orderbook_data
)

def enrich_ticker(ticker, asset_type, raw):
    fmp = get_fmp_data(ticker)
    finnhub = get_finnhub_indicators(ticker)
    lunar = get_lunarcrush_data(ticker)
    news = get_messari_news(ticker)
    santiment = get_santiment_correlation(ticker)
    orderbook = get_orderbook_data(ticker)

    price = f"{fmp['price']:.2f}"
    entry = f"{fmp['previousClose']:.2f}"
    stop = f"{fmp['dayLow']:.2f}"
    target1 = f"{fmp['dayHigh']:.2f}"
    target2 = f"{fmp['yearHigh']:.2f}"
    vol_spike = f"{fmp['volume']}"
    exchange = fmp.get("exchange", "Unknown")

    rsi = f"{finnhub['rsi']:.2f}"
    macd = "Bullish" if finnhub["macd_histogram"] > 0 else "Bearish"
    ema_stack = "Yes" if finnhub["ema_stack"] else "No"
    vwap_reclaim = "Yes" if fmp["price"] > finnhub["vwap"] else "No"

    btc_correlation = f"{santiment['correlation']:.2f}"
    orderbook_wall = orderbook["wall"]
    orderbook_exchange = orderbook["exchange"]

    sentiment_surge = f"{lunar['social_volume_change']}%"
    sentiment_analysis = lunar["summary"]
    sentiment_link = lunar["url"]

    catalyst = news["title"]
    catalyst_link = news["url"]

    risk_level = "High" if float(rsi) > 65 else "Medium" if float(rsi) > 50 else "Low"
    confidence = "Strong" if macd == "Bullish" and ema_stack == "Yes" else "Moderate"
    ai_score = f"{(float(rsi) + lunar['galaxyScore']) / 2:.2f}"
    ai_validation = "High" if macd == "Bullish" and float(rsi) > 50 and lunar["galaxyScore"] > 70 else "Medium"

    return {
        "ticker": ticker,
        "asset_type": asset_type,
        "price": price,
        "entry": entry,
        "stop": stop,
        "target1": target1,
        "target2": target2,
        "vol_spike": vol_spike,
        "rsi": rsi,
        "macd": macd,
        "ema_stack": ema_stack,
        "vwap_reclaim": vwap_reclaim,
        "orderbook_wall": orderbook_wall,
        "orderbook_exchange": orderbook_exchange,
        "btc_correlation": btc_correlation,
        "exchange": exchange,
        "sentiment_surge": sentiment_surge,
        "catalyst": catalyst,
        "sentiment_analysis": sentiment_analysis,
        "risk_level": risk_level,
        "confidence": confidence,
        "ai_score": ai_score,
        "ai_validation": ai_validation,
        "chart_link": f"https://www.tradingview.com/symbols/{ticker.replace('/', '')}",
        "catalyst_link": catalyst_link,
        "catalyst_link_text": "Messari",
        "sentiment_link": sentiment_link,
        "timestamp": datetime.now(ZoneInfo("Europe/London")).strftime("%Y-%m-%d %H:%M"),
        "type": raw["type"]
    }
