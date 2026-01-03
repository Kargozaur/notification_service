from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from core.settings import settings

SQL_ALCHEMY_URL = settings.DATABASE_URL

engine = create_async_engine(
    url=SQL_ALCHEMY_URL, max_overflow=10, future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
)  # ty:ignore[no-matching-overload]


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
