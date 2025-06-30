from dataclasses import dataclass
import datetime

from ...domain.models import User
from ...domain.repositories import UsersRepository
from ...domain.services import PasswordHashingService
from ...domain.value_objects import UserEmailAddress, PlainPassword
from ...domain.exceptions import UserAlreadyExistsException


@dataclass
class RegisterUserCommand:
    first_name: str
    last_name: str
    email_address: str
    password: str


@dataclass
class RegisterUserResponse:
    user_id: int
    first_name: str
    last_name: str
    email_address: str
    created_at: datetime


class RegisterUserUseCase:
    def __init__(
        self,
        users_repository: UsersRepository,
        password_hashing_service: PasswordHashingService,
    ):
        self._users_repository = users_repository
        self._password_hashing_service = password_hashing_service

    def execute(self, command: RegisterUserCommand) -> RegisterUserResponse:
        email_address = UserEmailAddress(value=command.email_address)
        plain_password = PlainPassword(value=command.password)

        if self._users_repository.exists_by_email(email_address):
            raise UserAlreadyExistsException(
                f"User with email {email_address.value} already exists"
            )

        hashed_password = self._password_hashing_service.hash_password(plain_password)

        user = User.create(
            first_name=command.first_name,
            last_name=command.last_name,
            email_address=email_address,
            hashed_password=hashed_password,
        )
        saved_user = self._users_repository.save(user)

        return RegisterUserResponse(
            user_id=saved_user.get_id().value,
            first_name=saved_user.first_name(),
            last_name=saved_user.last_name(),
            email_address=saved_user.email_address().value,
            created_at=saved_user.created_at(),
        )
