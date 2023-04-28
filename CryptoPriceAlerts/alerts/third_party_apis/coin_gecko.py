import logging
import random
import requests
import traceback

from django.conf import settings
from alerts.models import Alert

logger = logging.getLogger(__name__)


class CoinGecko:

    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3/"

        self.coin_id_map = {
            Alert.Coin.BITCOIN: "bitcoin",
            Alert.Coin.ETHEREUM: "ethereum",
            Alert.Coin.TETHER: "tether",
            Alert.Coin.BINANCECOIN: "binancecoin",
            Alert.Coin.RIPPLE: "ripple",
            Alert.Coin.CARDANO: "cardano",
            Alert.Coin.DOGECOIN: "dogecoin",
        }

        self.coin_id_reverse_map = {
            coin_gecko_coin_id: coin_id
            for coin_id, coin_gecko_coin_id in self.coin_id_map.items()
        }

    def get_coin_gecko_coin_ids(self, coin_ids):
        # Convert ticker symbol stored by our
        # system to coin id recognised by coin gecko
        return [self.coin_id_map[coin_id] for coin_id in coin_ids]

    @staticmethod
    def mock_price_variation(price):
        offset = random.choice(range(85, 120, 5))
        return price * offset / 100

    def format_coins_market_data(self, coins_market_data):
        # Format response received from coin gecko
        result = {}
        for coin_market_data in coins_market_data:
            coin_id = self.coin_id_reverse_map.get(coin_market_data["id"])
            if not coin_id:
                continue
            current_price = coin_market_data["current_price"]
            if settings.MOCK_PRICE_VARIATION:
                current_price = self.mock_price_variation(current_price)
            result[coin_id] = {
                "current_price": current_price
            }
        return result

    def get_coins_market_data(self, coin_ids):
        log_tag = "CoinGecko.get_coins_market_data"
        coin_ids = self.get_coin_gecko_coin_ids(coin_ids)
        coins_market_url = "coins/markets/"
        params = {
            "ids": ",".join(coin_ids),
            "vs_currency": "USD",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": False
        }
        full_url = f"{self.base_url}{coins_market_url}"
        logger.info(f"{log_tag} Coin Gecko API Call. URL: {full_url}, Params: {params}")
        try:
            coins_market_response = requests.get(full_url, params=params)
        except Exception as xcptn:
            traceback.print_exc()
            logger.exception(f"{log_tag} An error occured while retrieving data from coin gecko. Error: {xcptn}")
            return []
        if coins_market_response.status_code != 200:
            logger.error(
                f"{log_tag} An error occured while retrieving data from "
                f"coin gecko. Response Status: {coins_market_response.status_code}. "
                f"Error Message: {coins_market_response.text}."
            )
            return []
        return self.format_coins_market_data(coins_market_response.json())
