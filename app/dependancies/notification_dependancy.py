from . import Depends
from . import get_db
from . import AsyncSession
from services.notification_service.notification_service import (
    NotificationService,
)
from services.notification_service.notification_pref_repo import (
    NotificationRepo,
)


async def get_notification_repo(db: AsyncSession = Depends(get_db)):
    return NotificationRepo(db)


async def get_notification_service(
    notification_repo=Depends(get_notification_repo),
):
    return NotificationService(notification_repo)
