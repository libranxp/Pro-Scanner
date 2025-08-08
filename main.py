# main.py
from scan.crypto_spi import run_crypto_scan
from scan.stock_spi import run_stock_scan
from core.execution_plan import should_run_scan
from utils.logger import log_info

def main():
    if should_run_scan():
        log_info("Starting EmeraldAlert scan...")
        run_crypto_scan()
        run_stock_scan()
        log_info("Scan completed successfully.")
    else:
        log_info("Scan skipped based on execution plan.")

if __name__ == "__main__":
    main()
