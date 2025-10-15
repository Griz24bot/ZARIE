import requests
import logging
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL
from robin_credentials import ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD
import robin_stocks as r

logger = logging.getLogger(__name__)

class CryptoAssetRegistry:
    def __init__(self):
        self.assets = {
            "Alpaca": [],
            "Robinhood": [],
            "Coinbase": []
        }

    def fetch_all(self):
        self.assets["Alpaca"] = self.fetch_alpaca_assets()
        self.assets["Robinhood"] = self.fetch_robinhood_assets()
        self.assets["Coinbase"] = self.fetch_coinbase_assets()

    def fetch_alpaca_assets(self):
        try:
            url = f"{ALPACA_BASE_URL}/v2/assets?asset_class=crypto"
            headers = {
                "APCA-API-KEY-ID": ALPACA_API_KEY,
                "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                assets = response.json()
                return [asset['symbol'] for asset in assets if asset['tradable']]
            else:
                logger.error(f"Alpaca assets fetch failed: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Alpaca assets fetch error: {e}")
            return []

    def fetch_robinhood_assets(self):
        try:
            # Robinhood supported cryptos (hardcoded as per feedback)
            return ["BTC", "ETH", "LTC", "DOGE", "ADA", "SOL", "SHIB", "XRP", "UNI", "AVAX", "PEPE", "TRUMP"]
        except Exception as e:
            logger.error(f"Robinhood assets fetch error: {e}")
            return []

    def fetch_coinbase_assets(self):
        try:
            # Coinbase API endpoint for assets might be different; using a valid one or fallback
            url = "https://api.coinbase.com/v2/currencies"
            response = requests.get(url)
            if response.status_code == 200:
                assets = response.json()
                return [asset['id'] for asset in assets.get('data', []) if asset.get('type') == 'crypto']
            else:
                logger.error(f"Coinbase assets fetch failed: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Coinbase assets fetch error: {e}")
            return []

    def get_common_assets(self):
        if not self.assets["Alpaca"] or not self.assets["Robinhood"] or not self.assets["Coinbase"]:
            self.fetch_all()
        return set(self.assets["Alpaca"]) & set(self.assets["Robinhood"]) & set(self.assets["Coinbase"])

    def get_platform_assets(self, platform):
        return self.assets.get(platform, [])
