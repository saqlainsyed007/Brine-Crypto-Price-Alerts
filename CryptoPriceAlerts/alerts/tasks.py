import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_email(to_emails, body):

    log_string = (
        f"\n==================================================================================\n"
        f"To: {to_emails}\n{body}"
        f"\n==================================================================================\n"
    )

    logger.info(log_string)
