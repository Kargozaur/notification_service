from abc import ABC, abstractmethod
from . import UUID


class NotificationSender(ABC):
    @abstractmethod
    async def send(
        self, user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]: ...
