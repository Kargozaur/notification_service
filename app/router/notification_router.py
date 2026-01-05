from . import Depends, APIRouter, NotificationService, Body, Request
from dependancies.notification_dependancy import (
    get_notification_service,
)
from schemas.schemas import (
    NotificationPreferanceRead,
    UpdateNotificationPref,
    CreateNotification,
)
from oauth.oauth import get_current_user
from lifespan import limiter

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=NotificationPreferanceRead)
@limiter.limit("40/hour")
@limiter.limit("5/minute")
async def get_preferance(
    request: Request,
    notification_service: NotificationService = Depends(
        get_notification_service
    ),
    current_user=Depends(get_current_user),
):
    return await notification_service.create_or_get_preferance(
        current_user.id
    )


@router.patch("/", response_model=NotificationPreferanceRead)
@limiter.limit("20/hour")
@limiter.limit("5/minute")
async def update_preferance(
    request: Request,
    new_data: UpdateNotificationPref = Body(default=None),
    notification_service: NotificationService = Depends(
        get_notification_service
    ),
    current_user=Depends(get_current_user),
):
    if not new_data:
        return await notification_service.create_or_get_preferance(
            current_user.id
        )

    return await notification_service.update_preferance(
        current_user.id, new_data
    )


@router.post("/notify")
@limiter.limit("100/hour")
@limiter.limit("10/minute")
async def send_notification(
    request: Request,
    payload: CreateNotification = Body(default=None),
    notification_service: NotificationService = Depends(
        get_notification_service
    ),
    current_user=Depends(get_current_user),
):
    result = await notification_service.notify(
        current_user.id, payload.title, payload.body, payload.channel
    )
    return result


# @router.post("/", response_model=NotificationPreferanceRead)
# async def create_preferance(
#     notification_service=Depends(get_notification_service),
#     current_user=Depends(get_current_user),
# ):
#     return await notification_service.create_or_get_preferance(
#         current_user.id
#     )
