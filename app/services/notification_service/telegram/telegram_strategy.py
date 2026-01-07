from uuid import UUID
import logging
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramAPIError
from core.settings import settings
from .. import NotificationSender

logger = logging.getLogger(__name__)


class TelegramSender(NotificationSender):
    def __init__(self, channel_id: str | int) -> None:
        self.channel_id = channel_id

    async def send(
        self, user_id: UUID, title: str, body: str
    ) -> tuple[bool, str | None]:
        bot = Bot(
            token=settings.TELEGRAM_TOKEN,
            default=DefaultBotProperties(parse_mode=None),
        )
        text = f"{user_id}: \n title: {title} \n body: {body}"
        try:
            await bot.send_message(
                chat_id=self.channel_id,
                text=text,
                parse_mode=None,
                disable_notification=True,
            )
            return True, None
        except TelegramAPIError as exc:
            text = str(exc)
            logger.warning(f"Exception occured: {text}")
            return False, text
        except Exception as exc:
            text = str(exc)
            logger.exception(f"Global error -> {exc}")
            return False, text
        finally:
            await bot.session.close()
