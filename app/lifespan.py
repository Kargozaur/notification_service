from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker
from contextlib import asynccontextmanager
from database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.async_session = async_sessionmaker(engine)

    yield
    await engine.dispose()
