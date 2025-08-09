# provider_registry.py
import os
from utils.logger import log

PROVIDERS = {
    "coinmarketcap": {
        "key": os.getenv("CMC_KEY"),
        "module": "apis.coinmarketcap",
        "status": "unknown"
    },
    "coingecko": {
        "key": None,
        "module": "apis.coingecko",
        "status": "unknown"
    },
    "coinglass": {
        "key": os.getenv("COINGLASS_KEY"),
        "module": "apis.coinglass",
        "status": "unknown"
    },
    "binance": {
        "key": None,
        "module": "apis.binance",
        "status": "unknown"
    },
    "finnhub": {
        "key": os.getenv("FINNHUB_KEY"),
        "module": "apis.finnhub",
        "status": "unknown"
    },
    "alpha_vantage": {
        "key": os.getenv("ALPHAVANTAGE_KEY"),
        "module": "apis.alpha_vantage",
        "status": "unknown"
    },
    "lunarcrush": {
        "key": os.getenv("LUNARCRUSH_KEY"),
        "module": "apis.lunarcrush",
        "status": "unknown"
    },
    "twitter_sentiment": {
        "key": None,
        "module": "apis.twitter_sentiment",
        "status": "unknown"
    }
}

def mark_provider_status(name, status):
    if name in PROVIDERS:
        PROVIDERS[name]["status"] = status
        log(f"🔍 Provider '{name}' marked as {status}")
    else:
        log(f"⚠️ Unknown provider: {name}")

def get_provider_module(name):
    return PROVIDERS.get(name, {}).get("module")

def get_provider_status(name):
    return PROVIDERS.get(name, {}).get("status", "unknown")

def list_provider_statuses():
    return {name: data["status"] for name, data in PROVIDERS.items()}
