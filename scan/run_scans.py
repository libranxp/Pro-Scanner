import sys
import os

# Ensure repo root is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scan.scan_stocks import scan_stock_assets
from scan.scan_crypto import scan_crypto  # Fixed import path

def run_all_scans():
    print("[Scanner] Starting stock and crypto scans...")  # Optional log line

    stock_symbols = ["TSLA", "NVDA", "AAPL", "GME", "PLTR"]
    crypto_symbols = ["BTC", "ETH", "SOL", "ADA", "DOGE"]

    scan_stock_assets(stock_symbols)
    scan_crypto(crypto_symbols)

if __name__ == "__main__":
    run_all_scans()
