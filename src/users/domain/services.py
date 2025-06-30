from abc import ABC, abstractmethod
from typing import Optional
from .value_objects import PlainPassword, HashedPassword


class PasswordHashingService(ABC):
    @abstractmethod
    def hash_password(self, plain_password: PlainPassword) -> HashedPassword: ...

    @abstractmethod
    def verify_password(
        self, plain_password: PlainPassword, hashed_password: HashedPassword
    ) -> bool: ...


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, user_id: int) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> Optional[int]: ...
