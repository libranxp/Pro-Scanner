import os
import requests

def fetch_crypto_data(symbol: str):
    cmc_key = os.getenv("CMC_KEY")
    cmcal_key = os.getenv("CMCAL_KEY")
    lunar_key = os.getenv("LUNARCRUSH_KEY")
    messari_key = os.getenv("MESSARI_KEY")

    headers_cmc = {"X-CMC_PRO_API_KEY": cmc_key}
    headers_cal = {"Authorization": cmcal_key}
    headers_lunar = {"Authorization": f"Bearer {lunar_key}"}
    headers_messari = {"x-messari-api-key": messari_key}

    responses = {}

    # CoinMarketCap
    cmc_url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}"
    responses["cmc"] = requests.get(cmc_url, headers=headers_cmc).json()

    # Messari Profile
    messari_url = f"https://data.messari.io/api/v1/assets/{symbol}/profile"
    responses["messari"] = requests.get(messari_url, headers=headers_messari).json()

    # LunarCrush
    lunar_url = f"https://api.lunarcrush.com/v2?data=assets&key={lunar_key}&symbol={symbol}"
    responses["lunar"] = requests.get(lunar_url, headers=headers_lunar).json()

    # CoinMarketCal Events
    cmcal_url = f"https://developers.coinmarketcal.com/v1/events?coins={symbol}&sortBy=date"
    responses["cmcal"] = requests.get(cmcal_url, headers=headers_cal).json()

    return responses
