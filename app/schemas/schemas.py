from datetime import time, timezone
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    ConfigDict,
)
from typing import Annotated, Optional
from utility.validate_fields import (
    validate_email_no_emoji,
    validate_password_allow_unicode_but_no_emoji,
    validate_phone_no_emoji,
    validate_username_no_emoji,
)
import uuid
import re
from enum import StrEnum


class NotificationsEnum(StrEnum):
    telegram = "telegram"
    email = "email"
    web_push = "web-push"


class CreateUser(BaseModel):
    email: EmailStr
    password: Annotated[
        str,
        Field(
            ...,
            min_length=8,
            description="Password must contain at least 1 upper case \n"
            "1 number, 1 special character",
        ),
    ]
    username: str
    phone_number: PhoneNumber

    @field_validator("password")
    @classmethod
    def verify_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("password.uppercase_required")
        if not re.search(r"\d", value):
            raise ValueError("password.number_required")
        if not re.search(r"[!@#$%^&*(),.:<>|?]", value):
            raise ValueError("password.specialsymbol_required")
        return value

    @field_validator("password")
    @classmethod
    def check_password(cls, v):
        return validate_password_allow_unicode_but_no_emoji(v)

    @field_validator("email")
    @classmethod
    def check_email(cls, v):
        return validate_email_no_emoji(v)

    @field_validator("phone_number")
    @classmethod
    def check_number(cls, v):
        return validate_phone_no_emoji(v)

    @field_validator("username")
    @classmethod
    def check_username(cls, v):
        return validate_username_no_emoji(v)


class LoginUser(BaseModel):
    email: str
    password: str


class NotificationPreferanceCreate(BaseModel):
    preferred_channel: NotificationsEnum
    quiet_hours_start: Optional[time] = time(
        hour=23, minute=0, second=0, tzinfo=timezone.utc
    )
    quiet_hours_end: Optional[time] = time(
        hour=7, minute=30, second=0, tzinfo=timezone.utc
    )
    channel_specific_settings: dict = Field(..., default_factory=dict)
    email_enabled: Optional[bool] = True
    push_enabled: Optional[bool] = True
    telegram_enabled: Optional[bool] = True


class UpdateNotificationPref(BaseModel):
    preffered_channel: Optional[NotificationsEnum] = None
    quite_hours_start: Optional[time] = None
    quite_hours_end: Optional[time] = None
    email_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None
    telegram_enabled: Optional[bool] = None


class NotificationPreferanceRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    preferred_channel: NotificationsEnum
    quiet_hours_start: time
    quiet_hours_end: time
    channel_specific_settings: dict
    email_enabled: bool
    push_enabled: bool
    telegram_enabled: bool

    model_config = ConfigDict(from_attributes=True)


class CreateNotification(BaseModel):
    title: str
    body: str
    channel: str | None = None


class TokenPayload(BaseModel):
    sub: uuid.UUID | None = None
    exp: int | None = None
