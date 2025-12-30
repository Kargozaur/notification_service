from sqlalchemy.orm import DeclarativeBase, validates
from . import (
    Mapped,
    mapped_column,
    TIME,
    JSONB,
    declared_attr,
    re,
    camel_to_snake,
    text,
    String,
    datetime,
    time,
    TIMESTAMP,
    Boolean,
    relationship,
)
from .mixins import (
    UUIDPKMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    OwnedByMixin,
    NotificationPreferenceMixin,
    QueuedMixin,
    ChannelTypeMixin,
)


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__) + "s"


class User(UUIDPKMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(
        String(15),
    )
    username: Mapped[str] = mapped_column(String(32), unique=True)

    notification_preferences = relationship(
        "NotificationPreference",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    delivery_logs = relationship(
        "NotificationDeliveryLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    channel_configs = relationship(
        "ChannelConfig",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @validates("phone")
    def validate_phone(self, number: str) -> str:
        if not number:
            raise ValueError("You need to provide your phone number")
        cleared: str = "".join(number.split())
        pattern = r"^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"
        if not re.match(pattern, cleared):
            raise ValueError(
                "Phone number is not valid. Examples of valid formats: \n  +1 (234) 567-8901\n"
                "  1234567890\n"
                "  +44 20 1234 5678\n"
                "  123-456-7890"
            )
        return number


class NotificationPreference(
    UUIDPKMixin, OwnedByMixin, NotificationPreferenceMixin, Base
):
    preferred_channed: Mapped[str] = mapped_column(String(30))
    quiet_hours_start: Mapped[time] = mapped_column(
        TIME(timezone=True)
    )
    quiet_hours_end: Mapped[time] = mapped_column(TIME(timezone=True))

    channel_specific_settings: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict, server_default="{}"
    )


class NotificationDeliveryLog(
    UUIDPKMixin, OwnedByMixin, ChannelTypeMixin, QueuedMixin, Base
):
    notification_type: Mapped[str] = mapped_column(
        String(32), nullable=False
    )
    payload: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict, server_default="{}"
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    error_message: Mapped[str] = mapped_column(
        String(length=30), nullable=False
    )


class NotificationChannel(Base):
    type: Mapped[str] = mapped_column(String(32), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(30))
    requires_auth: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )
    default_settings: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default={}, server_default="{}"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )


class ChannelConfig(
    UUIDPKMixin, OwnedByMixin, ChannelTypeMixin, Base
):
    credentials: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict, server_default="{}"
    )
    settings: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict, server_default="{}"
    )
    is_valid: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false")
    )
    last_visited_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(),
        server_default=text("now()"),
    )
