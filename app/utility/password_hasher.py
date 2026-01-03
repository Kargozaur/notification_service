from abc import ABC, abstractmethod
import bcrypt
import hashlib


class IPasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, user_password) -> str:
        pass

    @abstractmethod
    def verify_password(
        self, user_password: str, db_password: str
    ) -> bool:
        pass


class PasswordHasher(IPasswordHasher):
    def hash_password(self, user_password: str) -> str:
        sha = hashlib.sha256(user_password.encode()).digest()
        return bcrypt.hashpw(sha, bcrypt.gensalt()).decode()

    def verify_password(
        self, user_password: str, db_password: str
    ) -> bool:
        sha = hashlib.sha256(user_password.encode()).digest()
        return bcrypt.checkpw(sha, db_password.encode())
