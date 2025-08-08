# utils/chart.py
def generate_chart_url(ticker, asset_type):
    base = "https://www.tradingview.com/chart/?symbol="
    prefix = "BINANCE:" if asset_type == "crypto" else ""
    return f"{base}{prefix}{ticker}"
