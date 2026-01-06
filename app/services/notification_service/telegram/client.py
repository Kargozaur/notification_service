from aiogram import Bot
from core.settings import settings

telegram_bot: Bot | None = None


async def init_bot() -> None:
    global telegram_bot

    telegram_bot = Bot(token=settings.TELEGRAM_TOKEN)


async def close_bot() -> None:
    global telegram_bot

    if telegram_bot is not None:
        await telegram_bot.session.close()
        telegram_bot = None
