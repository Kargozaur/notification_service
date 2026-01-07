from . import UUID
from . import NotificationSender


class EmailSender(NotificationSender):
    async def send(
        self, user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]:
        print(f"Sending for {user_id} with Email")
        print(f"       Title: {title}")
        print(f"       Body: {body}")
        print("     -> Success")
        return True, None


class MobilePushSender(NotificationSender):
    async def send(
        self, user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]:
        print(f"Sending for {user_id} with Push")
        print(f"       Title: {title}")
        print(f"       Body:{body}")
        print("     -> Success")
        return True, None
