from . import Depends, APIRouter, NotificationService
from dependancies.notification_dependancy import (
    get_notification_service,
)
from schemas.schemas import (
    NotificationPreferanceRead,
    UpdateNotificationPref,
)
from oauth.oauth import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=NotificationPreferanceRead)
async def get_preferance(
    notification_service: NotificationService = Depends(
        get_notification_service
    ),
    current_user=Depends(get_current_user),
):
    return await notification_service.create_or_get_preferance(
        current_user.id
    )


@router.patch("/", response_model=NotificationPreferanceRead)
async def update_preferance(
    new_data: UpdateNotificationPref,
    notification_service: NotificationService = Depends(
        get_notification_service
    ),
    current_user=Depends(get_current_user),
):
    return await notification_service.update_preferance(
        current_user.id, new_data
    )


# @router.post("/", response_model=NotificationPreferanceRead)
# async def create_preferance(
#     notification_service=Depends(get_notification_service),
#     current_user=Depends(get_current_user),
# ):
#     return await notification_service.create_or_get_preferance(
#         current_user.id
#     )
