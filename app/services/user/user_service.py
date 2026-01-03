from token_service import ITokenService
from user_repo import IUserRepositroy
from models.models import User
from schemas.schemas import CreateUser, LoginUser
from core.errors import UserAlreadyExists, UserNotFound
from utility.password_hasher import IPasswordHasher


class UserService:
    def __init__(
        self,
        user_repo: IUserRepositroy,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
    ) -> None:
        self.user = user_repo
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def check_user_exists(self, email: str) -> None:
        existing_user: (
            User | None
        ) = await self.user._get_user_by_email(email)
        if existing_user:
            raise UserAlreadyExists

    async def create_user(self, user_credential: CreateUser):
        await self.check_user_exists(user_credential.email)
        user: User = User(
            password=self.password_hasher.hash_password(
                user_credential.password
            ),
            email=user_credential.email,
            phone=user_credential.phone_number,
            username=user_credential.username,
        )
        new_user: User = await self.user.add_user(user)
        return new_user

    async def login_suer(self, user_credential: LoginUser):
        user: User | None = await self.user._get_user_by_email(
            user_credential.email
        )
        if not user:
            raise UserNotFound
        if not self.password_hasher.verify_password(
            user_credential.password, user.password
        ):
            raise UserNotFound

        access_token: str = self.token_service.create_token(user)
        return {"access_token": access_token, "token_type": "bearer"}
