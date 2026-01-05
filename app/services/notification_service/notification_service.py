from redis.asyncio import Redis
from . import UUID, timezone, datetime, time
from . import INotificationRepo, NotificationSender
from . import (
    NotificationPreferanceCreate,
    NotificationPreferanceRead,
    UpdateNotificationPref,
    NotificationsEnum,
)
from . import TelegramSender, EmailSender, MobilePushSender
from core.errors import (
    PreferanceDoesNotExists,
    ChannelDisabledError,
    QuietHoursError,
    NotificationTypeNotSupported,
)
import logging
from tasks.notification import send_notification

logger = logging.getLogger(__name__)


class NotificationService:
    """Methods for notification preferance are:
    create_or_get_preferance(user_id)
    update_preferance(user_id, user_data)
    """

    def __init__(
        self, notification_pref: INotificationRepo, redis: Redis
    ) -> None:
        self.notification_preferance = notification_pref
        self.redis = redis
        self.strategies: dict[str, NotificationSender] = {
            "email": EmailSender,
            "push": MobilePushSender,
            "telegram": TelegramSender,
        }

    async def _get_from_cached_helper(
        self, user_id: UUID
    ) -> NotificationPreferanceRead | None:
        """Helper method to extract data from cache if exists. Returns None if nothing found"""
        cached_key = f"notification:prefs:{user_id.hex}"
        try:
            cached = await self.redis.get(cached_key)
            if cached:
                return NotificationPreferanceRead.model_validate_json(
                    cached
                )
        except Exception as e:
            logger.warning(f"Redis unavailable {e}", exc_info=True)
        return None

    async def _invalidate_cache(self, user_id: UUID) -> None:
        cache_key = f"notification:prefs:{user_id.hex}"
        try:
            await self.redis.delete(cache_key)
            logger.debug(f"Cache invalidated for user {user_id}")
        except Exception as exc:
            logger.warning("Cache invalidation failed", exc_info=exc)

    async def _validate_time(self, start: time, end: time) -> bool:
        now = (
            datetime.now(tz=timezone.utc)
            .time()
            .replace(tzinfo=timezone.utc)
        )
        is_quiet: bool = (start <= end and start <= now <= end) or (
            start > end and (now >= start or now <= end)
        )
        return is_quiet

    async def get_channel(
        self, channel: str
    ) -> NotificationSender | None:
        sender = self.strategies.get("channel")
        if sender is None:
            NotificationTypeNotSupported
        return sender

    async def create_or_get_preferance(
        self, user_id: UUID
    ) -> NotificationPreferanceRead:
        """Tries to get preferance from cache, if not found, performs lookup in db.
        If nothing is found, an exception occures and a new preferance created."""

        search_cache = await self._get_from_cached_helper(user_id)
        if search_cache is not None:
            return search_cache
        try:
            pref = await self.notification_preferance.get_preferance(
                user_id
            )
        except PreferanceDoesNotExists:
            default_data = NotificationPreferanceCreate(
                preferred_channel=NotificationsEnum.email,
                channel_specific_settings={},
                email_enabled=True,
                push_enabled=True,
                telegram_enabled=False,
            )
            pref = (
                await self.notification_preferance.create_preferance(
                    user_id, default_data
                )
            )
        read_model = NotificationPreferanceRead.model_validate(pref)
        cached_key = f"notification:prefs{user_id}"
        try:
            await self.redis.set(
                cached_key, read_model.model_dump_json(), ex=600
            )
        except Exception as exc:
            logger.warning("Failed to cache preferance", exc_info=exc)
        return read_model

    async def update_preferance(
        self, user_id: UUID, user_data: UpdateNotificationPref
    ) -> NotificationPreferanceRead:
        """Tries to update data. If nothing to update tries to look up in cache.
        If nothing found in cache, looksup in DB.
        If user got no preferances, creates new for them."""
        to_update = user_data.model_dump(exclude_unset=True)
        if not to_update:
            current = await self.create_or_get_preferance(user_id)
            return current

        result = await self.notification_preferance.update_preferance(
            user_id, to_update
        )
        await self._invalidate_cache(user_id)
        return result

    async def notify(
        self,
        user_id: UUID,
        title: str,
        body: str,
        channel: str | None = None,
    ) -> dict:
        pref: NotificationPreferanceRead = (
            await self.create_or_get_preferance(user_id)
        )
        """If the user is currently in quiet time, the attempt to
            to send a notification is aborted.
        """
        is_quiet: bool = await self._validate_time(
            pref.quiet_hours_start, pref.quiet_hours_end
        )

        if is_quiet is True:
            raise QuietHoursError

        """Resolver for channel. If channel is None, set default from preferred channel"""
        channel_to_use: str = channel or pref.preferred_channel.value
        logger.info(f"{channel_to_use}")
        """Checks if channel is enabled. Raises if not"""
        match channel_to_use:
            case "email":
                enabled = pref.email_enabled
            case "telegram":
                enabled = pref.telegram_enabled
            case "push":
                enabled = pref.push_enabled
            case _:
                enabled = False
        if enabled is False:
            raise ChannelDisabledError

        send_notification.delay(user_id, title, body, channel_to_use)

        logging.info(
            f"Notification queued for user{user_id} via {channel_to_use}: title={title}"
        )
        return {"status": "queued", "channel": channel_to_use}
