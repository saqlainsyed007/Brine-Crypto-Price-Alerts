import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_email(to_emails, body):

    logger.info(f"To: {to_emails}")
    logger.info(body)
    logger.info(f"==================================================================================\n")
