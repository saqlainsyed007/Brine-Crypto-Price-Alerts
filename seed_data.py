import random

from django.contrib.auth.models import User
from alerts.models import Alert
from alerts.third_party_apis.coin_gecko import CoinGecko


coin_ids = [choice[0] for choice in Alert.Coin.CHOICES]

coin_gecko_api = CoinGecko()
coins_data = coin_gecko_api.get_coins_market_data(coin_ids)

user_1 = User.objects.create(
    username='alertsuser001', email="user.001@alertsemail.com"
)
user_1.set_password("password")
user_1.save()

user_2 = User.objects.create(
    username='alertsuser002',email="user.002@alertsemail.com"
)
user_2.set_password("password")
user_2.save()

for coin_id in coins_data:
    current_price = coins_data[coin_id]['current_price']
    for price_offset in range(85, 120, 5):
        users = [user_1, user_2]
        alert_price = current_price * price_offset / 100
        user = users.pop(random.choice([0, 1]))
        Alert.objects.create(
            coin_id=coin_id,
            alert_price=alert_price,
            user=user,
        )
        if random.choice([0, 0, 1]):
            user = set([user_1, user_2]).remove(user)
            Alert.objects.create(
                coin_id=coin_id,
                alert_price=alert_price,
                user=users[0],
            )
