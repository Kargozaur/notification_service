from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class CreateUser(BaseModel):
    email: EmailStr
    password: Annotated[
        str,
        Field(
            ...,
            min_length=8,
            pattern="(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9])",
            description="Password must contain at least 1 upper case \n"
            "1 number, 1 special character",
        ),
    ]
    username: str
    phone_number: PhoneNumber


class LoginUser(BaseModel):
    email: str
    password: str
