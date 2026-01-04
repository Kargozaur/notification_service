from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker
from contextlib import asynccontextmanager
from database import engine
from redis.asyncio import from_url
from core.logger import get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_logger()
    app.state.async_session = async_sessionmaker(engine)
    redis = from_url(
        url="redis://localhost:6379/0", decode_responses=True
    )
    app.state.redis = redis

    yield
    await engine.dispose()
    await redis.close()
