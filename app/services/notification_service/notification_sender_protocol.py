from typing import Protocol
from . import UUID


class NotificationSender(Protocol):
    @staticmethod
    async def send(
        user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]: ...
