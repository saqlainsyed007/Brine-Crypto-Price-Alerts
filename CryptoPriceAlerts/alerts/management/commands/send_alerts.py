import logging
import time

from django.core.cache import cache
from django.core.management.base import BaseCommand

from alerts.models import Alert
from alerts.third_party_apis.coin_gecko import CoinGecko
from alerts.utils import send_alerts

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:

            time.sleep(10)

            last_known_prices = cache.get("last_known_coin_prices", {})
            current_prices = {}

            coin_ids = Alert.objects.filter(
                alert_status=Alert.AlertStatus.CREATED
            ).distinct('coin_id').values_list("coin_id", flat=True)

            if not coin_ids:
                logger.info("No pending alerts to trigger")
                continue

            coin_gecko_api = CoinGecko()
            coins_data = coin_gecko_api.get_coins_market_data(coin_ids)
            for coin_id in coins_data:
                coin_data = coins_data[coin_id]
                last_known_prices[coin_id] = last_known_prices.get(coin_id, coin_data["current_price"])
                current_prices[coin_id] = coin_data["current_price"]
                send_alerts(
                    coin_id=coin_id,
                    previous_price=last_known_prices[coin_id],
                    current_price=current_prices[coin_id]
                )
            last_known_prices.update(current_prices)
            cache.set("last_known_coin_prices", last_known_prices)
