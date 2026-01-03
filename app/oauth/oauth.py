from fastapi import status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from schemas.schemas import TokenPayload
import uuid
from database import get_db
from models.models import User
from core.settings import settings
from core.errors import UserNotFound

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login", auto_error=False
)


def verify_access_token(
    token: str, credential_exception: Exception
) -> TokenPayload:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return TokenPayload(**payload)
    except Exception:
        raise credential_exception


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentai_exception: Exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unathorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentai_exception)
    if not token_data.sub:
        raise credentai_exception
    uid: uuid.UUID = token_data.sub
    user = await db.get(User, uid)
    if not user:
        raise UserNotFound
    return user
