from typing import Any
from core.settings import Settings
from datetime import datetime, timedelta
from jose import jwt
from abc import ABC, abstractmethod
from models.models import User


class ITokenService(ABC):
    @abstractmethod
    def create_token(self, user: User) -> str:
        pass


class TokenService(ITokenService):
    def __init__(self, settings: Settings) -> None:
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_ttl = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_token(self, user: User) -> str:
        to_encode: dict[str, Any] = {"sub": str(user.id)}
        expire: datetime = datetime.now() + timedelta(
            minutes=self.access_ttl
        )
        to_encode.update({"exp": expire})
        ecndoed: str = jwt.encode(
            claims=to_encode,
            key=self.secret_key,
            algorithm=[self.algorithm],
        )
        return ecndoed
