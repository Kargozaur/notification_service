import uuid
from . import INotificationRepo
from . import (
    NotificationPreferanceCreate,
    NotificationPreferanceRead,
    UpdateNotificationPref,
    NotificationsEnum,
)
from core.errors import PreferanceDoesNotExists


class NotificationService:
    """Methods for notification preferance are:
    create_or_get_preferance(user_id)
    update_preferance(user_id, user_data)
    """

    def __init__(self, notification_pref: INotificationRepo) -> None:
        self.notification_preferance = notification_pref

    async def create_or_get_preferance(
        self, user_id: uuid.UUID
    ) -> NotificationPreferanceRead:
        """Tries to get preferance, if none found raises exception and proceeds to creation of a new one."""
        try:
            return await self.notification_preferance.get_preferance(
                user_id
            )
        except PreferanceDoesNotExists:
            default_data = NotificationPreferanceCreate(
                preferred_channel=NotificationsEnum.email,
                channel_specific_settings={},
                email_enabled=True,
                push_enabled=True,
                telegram_enabled=True,
            )
            return (
                await self.notification_preferance.create_preferance(
                    user_id, default_data
                )
            )

    async def update_preferance(
        self, user_id: uuid.UUID, user_data: UpdateNotificationPref
    ) -> NotificationPreferanceRead:
        """if no data to update provided, tries to return existing data"""
        to_update = user_data.model_dump(exclude_unset=True)
        if not to_update:
            try:
                current = (
                    await self.notification_preferance.get_preferance(
                        user_id
                    )
                )
                return current
            except PreferanceDoesNotExists:
                raise PreferanceDoesNotExists
        result = await self.notification_preferance.update_preferance(
            user_id, to_update
        )
        return result
