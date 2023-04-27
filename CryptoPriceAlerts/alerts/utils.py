import logging

from django.utils import timezone
from alerts.models import Alert
from alerts.tasks import send_email

logger = logging.getLogger(__name__)


def send_alerts(coin_id, previous_price, current_price):

    logger.info(
        f"Sending alerts for {coin_id} for price change from {previous_price} to {current_price}"
    )

    if current_price == previous_price:
        logger.info(f"No price change for {coin_id}.")
        return

    filter_params = {
        "coin_id": coin_id,
        "alert_status": Alert.AlertStatus.CREATED,
    }

    # Filter all alerts after previous price and upto and including current price
    # Price has increased.
    if previous_price < current_price:
        price_alert_relation = "is now above"
        order_by_prefix = ''
        filter_params.update({
            'alert_price__gt': previous_price,
            'alert_price__lte': current_price,
        })
    # Price has decreased.
    if current_price < previous_price:
        price_alert_relation = "is now below"
        order_by_prefix = '-'
        filter_params.update({
            'alert_price__lt': previous_price,
            'alert_price__gte': current_price,
        })

    alerts = Alert.objects.filter(
        **filter_params
    ).select_related('user').order_by(f'{order_by_prefix}alert_price')

    if not alerts:
        logger.info(f"No pending alerts for {coin_id} from ${previous_price} to ${current_price}")
        return

    emails = [alerts[0].user.email]
    previous_alert_price = alerts[0].alert_price
    for alert in alerts[1:]:
        if previous_alert_price != alert.alert_price:
            email_content = f"{coin_id.title()} price alert. Price {price_alert_relation} {previous_alert_price}"
            send_email.delay(to_emails=emails, body=email_content)
            previous_alert_price = alert.alert_price
            emails = []
        emails.append(alert.user.email)
    price_alert_relation = "is now" if previous_alert_price == current_price else price_alert_relation
    email_content = f"{coin_id.title()} price alert. Price {price_alert_relation} {previous_alert_price}"
    send_email.delay(to_emails=emails, body=email_content)

    alerts.update(
        alert_status=Alert.AlertStatus.TRIGGERED,
        triggered_time=timezone.now(),
        updated=timezone.now(),
    )

    return alerts
