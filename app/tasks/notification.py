from services.notification_service.notification_strategies import (
    TelegramSender,
    MobilePushSender,
    EmailSender,
)

from celery import shared_task
from core.errors import SendChannelError
from asgiref.sync import async_to_sync

SENDER_MAP = {
    "email": EmailSender(),
    "push": MobilePushSender(),
    "telegram": TelegramSender(),
}


@shared_task(
    bind=True,
    name="send_notification",
)
def send_notification(self, user_id, title, body, channel):
    strategy = (
        SENDER_MAP.get(channel) if channel in SENDER_MAP else None
    )
    if strategy is None:
        raise SendChannelError
    try:
        success, error = async_to_sync(strategy.send)(
            user_id, title, body
        )  # ty:ignore[not-iterable]
    except Exception:
        raise
    if success:
        print(
            f"[Celery] sending through {channel} to {user_id}: {body}"
        )
        print("message from rabbitmq")
    else:
        raise SendChannelError
