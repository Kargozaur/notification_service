from celery import Celery
from core.settings import settings

celery = Celery(
    "tasks",
    broker=settings.RABBIT_MQ,
    backend=settings.REDIS_URL,
    include=["tasks.notification"],
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
