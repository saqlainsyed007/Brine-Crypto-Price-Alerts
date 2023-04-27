import logging

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from alerts.models import Alert

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Alert)
def alerts_clear_cache_post_save(sender, instance, created, **kwargs):    
    cache_keys_regex = f"alerts_user_{instance.user.id}_*"
    cache.delete_many(cache.keys(cache_keys_regex))
    logger.info(f"Deleted Alert List Cache for User {instance.user.id}")
