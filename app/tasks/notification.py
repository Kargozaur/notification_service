from services.notification_service.notification_strategies import (
    TelegramSender,
    MobilePushSender,
    EmailSender,
)

from celery import shared_task
from core.errors import SendChannelError
import logging

logger = logging.getLogger(__name__)


def get_class(channel):
    SENDER_MAP = {
        "email": EmailSender,
        "push": MobilePushSender,
        "telegram": TelegramSender,
    }
    cls = SENDER_MAP.get(channel)
    if cls is None:
        raise SendChannelError
    return cls()


@shared_task(
    bind=True,
    name="send_notification",
)
def send_notification(self, user_id, title, body, channel):
    strategy = get_class(channel)
    if strategy is None:
        raise SendChannelError
    try:
        success, error = strategy.send(user_id, title, body)  # ty:ignore[not-iterable]
    except Exception:
        raise
    if success:
        print(
            f"[Celery] sending through {channel} to {user_id}: {body}"
        )
        print("message from rabbitmq")
    else:
        raise SendChannelError
