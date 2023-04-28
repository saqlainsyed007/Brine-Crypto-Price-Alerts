import logging

from django.core.cache import cache
from django.utils import timezone
from alerts.models import Alert
from alerts.tasks import send_email
from alerts.views import AlertListCreateAPIView

logger = logging.getLogger(__name__)


def clear_list_alerts_cache(user_ids):
    log_tag = "alerts.utils.clear_list_alerts_cache"
    for user_id in user_ids:
        cache_key_template = AlertListCreateAPIView.cache_key_template
        cache_keys_regex = cache_key_template.format(
            user_id=user_id, alert_status="*", page_number="*"
        )
        cache.delete_many(cache.keys(cache_keys_regex))
        logger.info(f"{log_tag} Deleted alert list cache for user {user_id}")


def send_alerts(coin_id, previous_price, current_price):

    log_tag = "alerts.utils.send_alerts"

    if current_price == previous_price:
        logger.info(f"{log_tag} No price change for {coin_id}.")
        return

    logger.info(
        f"{log_tag} Send alerts for {coin_id} for price change from {previous_price} to {current_price}"
    )

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
        logger.info(
            f"{log_tag} No pending alerts for {coin_id} from ${previous_price} to ${current_price}"
        )
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

    logger.info(f"{log_tag} Alerts triggered: {alerts.values_list('id', flat=True)}")

    # !!! IMPORTANT !!!
    # alerts queryset was filtered with 'alert status: created' Once we
    # update the queryset with 'alert status: triggered', we will lose these
    # objects in the queryset because the values of the filter params in the
    # underlying objects have changed and thus alerts filter query will return no objects.
    # Get the user ids before the update.
    alerted_user_ids = list(alerts.values_list("user_id", flat=True))

    alerts.update(
        alert_status=Alert.AlertStatus.TRIGGERED,
        triggered_time=timezone.now(),
        updated=timezone.now(),
    )

    clear_list_alerts_cache(alerted_user_ids)
