from abc import ABC, abstractmethod
from typing import Optional

from src.shared.domain.value_objects import Id
from .value_objects import UserEmailAddress
from .models import User


class UsersRepository(ABC):
    @abstractmethod
    def all(self) -> list[User]: ...

    @abstractmethod
    def save(self, user: User) -> None: ...

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def find_by_email(self, email: UserEmailAddress) -> Optional[User]: ...

    @abstractmethod
    def exists_by_email(self, email: UserEmailAddress) -> bool: ...

    @abstractmethod
    def exists_by_id(self, id: Id) -> bool: ...
