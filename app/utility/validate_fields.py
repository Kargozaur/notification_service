import emoji


def validate_email_no_emoji(email: str) -> str:
    if emoji.emoji_count(email) > 0:
        raise ValueError("Email cannot contain emojis")
    return email


def validate_phone_no_emoji(phone: str) -> str:
    if emoji.emoji_count(phone) > 0:
        raise ValueError("Phone number cannot contain emojis")
    return phone


def validate_password_allow_unicode_but_no_emoji(pwd: str) -> str:
    if emoji.emoji_count(pwd) > 0:
        raise ValueError("Password cannot contain emojis")
    return pwd


def validate_username_no_emoji(username: str) -> str:
    if emoji.emoji_count(username) > 0:
        raise ValueError("Username can not contain emojis")
    return username
