from typing import Protocol
from . import UUID


class NotificationSender(Protocol):
    async def send(
        self, user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]: ...
