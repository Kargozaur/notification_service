from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from . import INotificationRepo
from schemas.schemas import (
    NotificationPreferanceCreate,
    NotificationPreferanceRead,
)
from models.models import NotificationPreferance
from core.errors import PreferanceDoesNotExists


class NotificationRepo(INotificationRepo):
    def __init__(self, db: AsyncSession) -> None:
        self._db_session = db

    def _get_preferance_query(self, user_id: uuid.UUID):
        return select(NotificationPreferance).where(
            NotificationPreferance.user_id == user_id
        )

    async def _get_current_or_raise(
        self, user_id
    ) -> NotificationPreferance:
        """ ""Helper function to get preferance of the user.
        Raises if not found"""
        query = self._get_preferance_query(user_id)
        result = await self._db_session.execute(query)
        pref = result.scalar_one_or_none()
        if pref is None:
            raise PreferanceDoesNotExists
        return pref

    async def create_preferance(
        self,
        user_id: uuid.UUID,
        preferances: NotificationPreferanceCreate,
    ) -> NotificationPreferanceRead:
        """
        Checks if preferance of the user already exists.
        Returns if exists, else raises exception and proceeds to creation
        """
        try:
            exists_pref = await self._get_current_or_raise(user_id)

            return NotificationPreferanceRead.model_validate(
                exists_pref
            )
        except PreferanceDoesNotExists:
            new_preferances = NotificationPreferance(
                user_id=user_id, **preferances.model_dump()
            )
            self._db_session.add(new_preferances)
            await self._db_session.commit()
            await self._db_session.refresh(new_preferances)
            query = self._get_preferance_query(user_id)
            refreshed = await self._db_session.execute(query)
            return NotificationPreferanceRead.model_validate(
                refreshed.scalar_one()
            )

    async def get_preferance(
        self, user_id: uuid.UUID
    ) -> NotificationPreferanceRead:
        """Tries to get user preferance. Raises if not found"""
        result = await self._get_current_or_raise(user_id)
        return NotificationPreferanceRead.model_validate(result)

    async def update_preferance(
        self, user_id: uuid.UUID, updated_pref: dict
    ) -> NotificationPreferanceRead:
        """Checks if user provided data to update. If not tries to return current. Raises if not found
        If user provided data, but preferance is not found raises.
        Returns new record if everything is ok.
        """
        if not updated_pref:
            current = await self._get_current_or_raise(user_id)
            return NotificationPreferanceRead.model_validate(current)
        await self._get_current_or_raise(user_id)
        update_st = (
            update(NotificationPreferance)
            .values(**updated_pref)
            .where(NotificationPreferance.user_id == user_id)
            .returning(NotificationPreferance)
        )
        result = await self._db_session.execute(update_st)
        updated = result.scalar_one()
        await self._db_session.commit()
        await self._db_session.refresh(updated)
        return NotificationPreferanceRead.model_validate(updated)
