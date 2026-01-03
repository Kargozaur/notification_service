from . import (
    mapped_column,
    Mapped,
    relationship,
    declared_attr,
    TIMESTAMP,
    ForeignKey,
    UUID,
    datetime,
    Boolean,
    text,
    String,
)
import uuid


class UUIDPKMixin:
    """Generic class for the tables with UUID as pk"""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )


class OwnedByMixin:
    """Adds user_id + relathionship to User"""

    @declared_attr
    def user_id(cls) -> Mapped[uuid.UUID | None]:
        return mapped_column(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=True,
            index=True,
        )

    @declared_attr
    def user(cls) -> Mapped["User | None"]:  # noqa: F821  # ty:ignore[unresolved-reference]
        return relationship(
            "User",
            back_populates=f"{cls.__tablename__}",  # ty:ignore[unresolved-attribute]
        )


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        default=datetime.now(),
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        default=datetime.now(),
    )


class NotificationPreferenceMixin:
    """Preferences for the notifications,
    All preferences are disabled by default
    """

    email_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        index=True,
        default=False,
        server_default=text("false"),
    )
    push_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        index=True,
        default=False,
        server_default=text("false"),
    )
    telegram_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        index=True,
        default=False,
        server_default=text("false"),
    )


class QueuedMixin:
    queued_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True)
    )
    sent_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True)
    )
    delievered_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True)
    )


class ChannelTypeMixin:
    channel_type: Mapped[str] = mapped_column(
        String(32), nullable=False
    )
