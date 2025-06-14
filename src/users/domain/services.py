from abc import ABC, abstractmethod
from .value_objects import PlainPassword, HashedPassword


class PasswordHashingService(ABC):
    @abstractmethod
    def hash_password(self, plain_password: PlainPassword) -> HashedPassword: ...

    @abstractmethod
    def verify_password(
        self, plain_password: PlainPassword, hashed_password: HashedPassword
    ) -> bool: ...
