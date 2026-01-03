from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Annotated
from utility.validate_fields import (
    validate_email_no_emoji,
    validate_password_allow_unicode_but_no_emoji,
    validate_phone_no_emoji,
    validate_username_no_emoji,
)
import uuid
import re


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


class TokenPayload(BaseModel):
    sub: uuid.UUID | None = None
    exp: int | None = None
