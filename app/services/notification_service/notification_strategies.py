from . import UUID


class TelegramSender:
    async def send(
        user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]:
        print(f"Sending for {user_id} with Telegram")
        print(f"       Title: {title}")
        print(f"       Body:{body}")
        print("     -> Success")
        return True, None


class EmailSender:
    async def send(
        user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]:
        print(f"Sending for {user_id} with Email")
        print(f"       Title: {title}")
        print(f"       Body: {body}")
        print("     -> Success")
        return True, None


class MobilePushSender:
    async def send(
        user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]:
        print(f"Sending for {user_id} with Push")
        print(f"       Title: {title}")
        print(f"       Body:{body}")
        print("     -> Success")
        return True, None
