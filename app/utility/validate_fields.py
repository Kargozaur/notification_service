import emoji
import re


def validate_email_no_emoji(email: str) -> str:
    if emoji.emoji_count(email) > 0:
        raise ValueError("Email cannot contain emojis")
    if re.search(r"[^a-zA-Z0-9@._\-]", email):
        raise ValueError(
            "Email can only contain letters, numbers, @ . _ -"
        )
    return email


def validate_phone_no_emoji(phone: str) -> str:
    if emoji.emoji_count(phone) > 0:
        raise ValueError("Phone number cannot contain emojis")
    return phone


def validate_password_allow_unicode_but_no_emoji(pwd: str) -> str:
    if emoji.emoji_count(pwd) > 0:
        raise ValueError("Password cannot contain emojis")
    if len(pwd) < 8:
        raise ValueError("Password must be at least 8 characters")
    return pwd


def validate_username_no_emoji(username: str) -> str:
    if emoji.emoji_count(username) > 0:
        raise ValueError("Username can not contain emojis")
    return username
