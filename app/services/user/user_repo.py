from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from models.models import User


class IUserRepositroy(ABC):
    @abstractmethod
    async def add_user(self, user: User) -> User:
        pass

    async def _get_user_by_email(self, email: str) -> User | None:
        pass


class UserRepository(IUserRepositroy):
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def _get_user_by_email(self, email: str) -> User | None:
        query: Result = await self._db_session.execute(
            select(User).where(User.email == email)
        )
        result: User | None = query.scalar_one_or_none()
        return result

    async def add_user(self, user: User) -> User:
        self._db_session.add(user)
        await self._db_session.commit()
        return user
