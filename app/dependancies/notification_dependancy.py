from fastapi import Request
from . import Depends
from . import get_db
from . import AsyncSession
from . import Redis
from . import Annotated
from services.notification_service.notification_service import (
    NotificationService,
)
from services.notification_service.notification_pref_repo import (
    NotificationRepo,
)


async def get_redis(request: Request) -> Redis:
    return request.app.state.redis


async def get_notification_repo(db: AsyncSession = Depends(get_db)):
    return NotificationRepo(db)


async def get_notification_service(
    redis: Annotated[Redis, Depends(get_redis)],
    notification_repo=Depends(get_notification_repo),
):
    return NotificationService(
        notification_pref=notification_repo, redis=redis
    )
