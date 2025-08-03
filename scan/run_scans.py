import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scan.scan_stocks import scan_stock_assets
from scan_crypto import scan_crypto

def run_all_scans():
    stock_symbols = ["TSLA", "NVDA", "AAPL", "GME", "PLTR"]
    crypto_symbols = ["BTC", "ETH", "SOL", "ADA", "DOGE"]

    scan_stocks(stock_symbols)
    scan_crypto(crypto_symbols)

if __name__ == "__main__":
    run_all_scans()
