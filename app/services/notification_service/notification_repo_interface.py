from abc import ABC, abstractmethod
import uuid
from schemas.schemas import (
    NotificationPreferanceCreate,
    NotificationPreferanceRead,
)


class INotificationRepo(ABC):
    @abstractmethod
    async def create_preferance(
        self,
        user_id: uuid.UUID,
        preferances: NotificationPreferanceCreate,
    ) -> NotificationPreferanceRead:
        """user_id and preferance data required"""
        pass

    @abstractmethod
    async def get_preferance(
        self, user_id: uuid.UUID
    ) -> NotificationPreferanceRead:
        """user_id need to be provided"""
        pass

    @abstractmethod
    async def update_preferance(
        self,
        user_id: uuid.UUID,
        updated_pref: dict,
    ):
        """user_id and data to update required"""
        pass
