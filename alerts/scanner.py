from utils.api_wrappers import (
    get_fmp_data, get_finnhub_indicators, get_crypto_data,
    get_lunarcrush_data, get_messari_news, get_orderflow_data
)

def scan_stocks():
    tickers = get_fmp_data("screener")  # dynamically fetch stock tickers
    valid = []

    for ticker in tickers:
        fmp = get_fmp_data(ticker)
        finnhub = get_finnhub_indicators(ticker)
        news = get_messari_news(ticker)
        orderflow = get_orderflow_data(ticker)

        if not fmp or not finnhub or not news or not orderflow:
            continue

        if (
            0.01 <= fmp["price"] <= 50.00 and
            fmp["premarket_gap"] > 5 and
            fmp["rvol"] > 5.0 and
            fmp["float"] < 50_000_000 and
            fmp["short_interest"] > 15 and
            fmp["atr_spike"] > 1.5 and
            fmp["price"] > finnhub["vwap_5min"] and
            finnhub["ema_stack_5min"] and
            finnhub["macd_histogram"] > 0 and
            fmp["resistance_gap"] < 5 and
            news["title"] and
            orderflow["dark_pool"] > 1_000_000
        ):
            valid.append(ticker)

    return valid


def scan_crypto():
    tickers = get_crypto_data("list")  # dynamically fetch crypto tickers
    valid = []

    for ticker in tickers:
        crypto = get_crypto_data(ticker)
        finnhub = get_finnhub_indicators(ticker)
        lunar = get_lunarcrush_data(ticker)
        news = get_messari_news(ticker)

        if not crypto or not finnhub or not lunar or not news:
            continue

        price = crypto["price"]
        tier = 1 if price <= 0.5 else 2 if price <= 3 else 3 if price <= 15 else 4
        atr_threshold = [0.01, 0.05, 0.2, 0.5][tier - 1]

        if (
            crypto["change_1h"] > 10 and
            crypto["rvol"] > 5.0 and
            crypto["atr"] > atr_threshold and
            finnhub["ema_stack_1h"] and
            price > finnhub["vwap_1h"] and
            finnhub["macd_histogram"] > 0 and
            finnhub["stoch_rsi_crossover"] and
            finnhub["obv_confirmation"] and
            crypto["resistance_gap"] < 5 and
            news["title"] and
            crypto["whale_buy"] > 1_000_000 and
            crypto["stablecoin_inflow"] > 0 and
            crypto["short_liquidations"] > 0 and
            crypto["project_age_days"] >= 30 and
            crypto["legit_use_case"] and
            crypto["organic_volume"] and
            not crypto["token_unlocks"]
        ):
            valid.append(ticker)

    return valid
