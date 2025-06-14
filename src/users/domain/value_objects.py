from dataclasses import dataclass
import validators
import re

from shared.domain.exceptions import InvalidEmailAddressException
from .exceptions import WeakPasswordException


@dataclass(frozen=True, kw_only=True)
class Id:
    value: int

    def __post_init__(self) -> None:
        if self.value is None:
            raise ValueError("Id cannot be None")
        if not isinstance(self.value, int):
            raise ValueError("Id must be an integer")
        if self.value <= 0:
            raise ValueError("Id must be positive")

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if isinstance(other, Id):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass(frozen=True, kw_only=True)
class UserEmailAddress:
    value: str

    def __post_init__(self) -> None:
        if not validators.email(self.value):
            raise InvalidEmailAddressException


@dataclass(frozen=True, kw_only=True)
class HashedPassword:
    value: str

    def __post_init__(self) -> None:
        if not self.value or len(self.value) < 8:
            raise ValueError("Hashed password cannot be empty")


@dataclass(frozen=True, kw_only=True)
class PlainPassword:
    value: str

    def __post_init__(self) -> None:
        self._validate_password()

    def _validate_password(self) -> None:
        if len(self.value) < 8:
            raise WeakPasswordException(
                message="Password must be at least 8 characters long"
            )

        if not re.search(r"[A-Z]", self.value):
            raise WeakPasswordException(
                message="Password must contain at least one uppercase letter"
            )

        if not re.search(r"[a-z]", self.value):
            raise WeakPasswordException(
                message="Password must contain at least one lowercase letter"
            )

        if not re.search(r"\d", self.value):
            raise WeakPasswordException(
                message="Password must contain at least one digit"
            )

    def __str__(self) -> str:
        return "*" * len(self.value)
