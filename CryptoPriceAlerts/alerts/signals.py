import logging

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from alerts.models import Alert
from alerts.utils import clear_list_alerts_cache
from alerts.views import AlertListCreateAPIView

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Alert)
def alerts_clear_cache_post_save(sender, instance, created, **kwargs):
    clear_list_alerts_cache([instance.user_id])
