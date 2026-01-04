from . import Depends
from . import AsyncSession
from . import TokenService
from . import UserRepository
from . import UserService
from . import PasswordHasher
from core.settings import Settings
from . import get_db


async def get_user_repo(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)


async def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


async def get_settings() -> Settings:
    return Settings()  # ty:ignore[missing-argument]


async def get_token_service(
    settings: Settings = Depends(get_settings),
) -> TokenService:
    return TokenService(settings)


async def get_user_service(
    repo: UserRepository = Depends(get_user_repo),
    password: PasswordHasher = Depends(get_password_hasher),
    token_service: TokenService = Depends(get_token_service),
) -> UserService:
    return UserService(repo, password, token_service)
