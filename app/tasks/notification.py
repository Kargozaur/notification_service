from services.notification_service.telegram.telegram_strategy import (
    TelegramSender,
)
from services.notification_service.notification_strategies import (
    MobilePushSender,
    EmailSender,
)
from celery import shared_task
from core.errors import SendChannelError
import logging
import asyncio
from core.settings import settings

logger = logging.getLogger(__name__)


def get_strategy(channel):
    SENDER_MAP = {
        "email": EmailSender,
        "push": MobilePushSender,
        "telegram": TelegramSender,
    }
    cls = SENDER_MAP.get(channel)
    if cls is None:
        raise SendChannelError
    """Currently harcdoed for test purposes"""
    return cls(settings.TELEGRAM_CHANNEL)


@shared_task(
    bind=True,
    name="send_notification",
    max_retries=3,
    default_retry_delay=30,
    retry_backoff=True,
)
def send_notification(self, user_id, title, body, channel):
    strategy = get_strategy(channel)
    if strategy is None:
        raise SendChannelError

    try:
        success, error = asyncio.run(
            strategy.send(user_id, title, body)
        )
        if not success:
            raise SendChannelError
        logger.info(
            f"Notification sent successfully for user {user_id}"
        )
    except SendChannelError:
        logger.warning(
            f"Send failed, will retry {channel}, {user_id}"
        )

    except Exception:
        logger.exception("An error occured")
        raise
