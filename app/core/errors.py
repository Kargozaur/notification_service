from fastapi import status, HTTPException


class DomainError(Exception):
    message: str = "An error occured"
    status_code: int = status.HTTP_400_BAD_REQUEST

    def to_HTTP(self) -> HTTPException:
        return HTTPException(
            status_code=self.status_code, detail=self.message
        )


class UserAlreadyExists(DomainError):
    """Exception class when trying to add user with email that's already in the db"""

    message: str = "User already exists"
    status_code = status.HTTP_409_CONFLICT


class UserNotFound(DomainError):
    message: str = "User with this credentials is not found"
    status_code = status.HTTP_404_NOT_FOUND


class PreferanceDoesNotExists(DomainError):
    message: str = (
        "Preferances for this user doesn't exist, please create them"
    )
    status_code = status.HTTP_404_NOT_FOUND


class ChannelDisabledError(DomainError):
    message: str = (
        "Please enable this channel before sending anything to it"
    )
    status_code = status.HTTP_409_CONFLICT


class QuietHoursError(DomainError):
    message: str = "User has quiet hours now"
    status_code = status.HTTP_425_TOO_EARLY
