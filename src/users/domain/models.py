from datetime import datetime
from typing import Optional

from src.shared.domain.value_objects import Id

from .value_objects import UserEmailAddress, HashedPassword


class User:
    def __init__(
        self,
        email_address: UserEmailAddress,
        hashed_password: HashedPassword,
        id: Optional[Id] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._id = id
        self._email_address = email_address
        self._hashed_password = hashed_password
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or datetime.now()

    @classmethod
    def create(
        cls,
        email_address: UserEmailAddress,
        hashed_password: HashedPassword,
    ) -> "User":
        return cls(
            email_address,
            hashed_password=hashed_password,
        )

    @classmethod
    def from_persistence(
        cls,
        id: Id,
        email_address: UserEmailAddress,
        hashed_password: HashedPassword,
        created_at: datetime,
        updated_at: datetime,
    ) -> "User":
        return cls(
            id=id,
            email_address=email_address,
            hashed_password=hashed_password,
            created_at=created_at,
            updated_at=updated_at,
        )

    def get_id(self) -> Optional[Id]:
        return self._id

    def email_address(self) -> UserEmailAddress:
        return self._email_address

    def hashed_password(self) -> HashedPassword:
        return self._hashed_password

    def created_at(self) -> datetime:
        return self._created_at

    def updated_at(self) -> datetime:
        return self._updated_at

    def is_persisted(self) -> bool:
        return self._id is not None

    def _assign_id(self, user_id: Id) -> None:
        """
        Internal method for assigning IDs when persisting.
        It should only be called from the repository.
        """
        if self._id is not None:
            raise ValueError("Cannot reassign ID to an already persisted user")
        self._id = user_id

    def __str__(self) -> str:
        id_str = str(self._id.value) if self._id else "NEW"
        return f"User(id={id_str}, email={self._email_address.value})"
