from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker
from contextlib import asynccontextmanager
from database import engine
from redis.asyncio import from_url
from core.logger import get_logger
from core.settings import settings
from slowapi.util import get_remote_address
from slowapi import Limiter
from services.notification_service.telegram.client import (
    init_bot,
    telegram_bot,
    close_bot,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_logger()
    app.state.async_session = async_sessionmaker(engine)
    redis = from_url(url=settings.REDIS_URL, decode_responses=True)
    app.state.redis = redis
    await init_bot()
    app.state.bot = telegram_bot

    yield
    await engine.dispose()
    await redis.close()
    await close_bot()


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["20/minute"],
    storage_uri=settings.REDIS_URL,
)
