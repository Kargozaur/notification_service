from typing import Protocol
from . import UUID


class NotificationSender(Protocol):
    @staticmethod
    def send(
        user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]: ...
