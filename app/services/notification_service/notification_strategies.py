from . import UUID


class EmailSender:
    @staticmethod
    def send(
        user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]:
        print(f"Sending for {user_id} with Email")
        print(f"       Title: {title}")
        print(f"       Body: {body}")
        print("     -> Success")
        return True, None


class MobilePushSender:
    @staticmethod
    def send(
        user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]:
        print(f"Sending for {user_id} with Push")
        print(f"       Title: {title}")
        print(f"       Body:{body}")
        print("     -> Success")
        return True, None
