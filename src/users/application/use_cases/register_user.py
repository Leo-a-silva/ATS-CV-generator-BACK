from dataclasses import dataclass

from ...domain.models import User
from ...domain.repositories import UsersRepository
from ...domain.services import PasswordHashingService
from ...domain.value_objects import UserEmailAddress, PlainPassword
from ...domain.exceptions import UserAlreadyExistsException


@dataclass
class RegisterUserCommand:
    email: str
    password: str


@dataclass
class RegisterUserResponse:
    user_id: int
    email: str
    created_at: str


class RegisterUserUseCase:
    def __init__(
        self,
        users_repository: UsersRepository,
        password_hashing_service: PasswordHashingService,
    ):
        self._users_repository = users_repository
        self._password_hashing_service = password_hashing_service

    def execute(self, command: RegisterUserCommand) -> RegisterUserResponse:
        email = UserEmailAddress(value=command.email)
        plain_password = PlainPassword(value=command.password)

        if self._users_repository.exists_by_email(email):
            raise UserAlreadyExistsException(f"User with email {email} already exists")

        hashed_password = self._password_hashing_service.hash_password(plain_password)

        user = User.create(email=email, hashed_password=hashed_password)
        saved_user = self._users_repository.save(user)

        return RegisterUserResponse(
            user_id=saved_user.id.value,
            email=saved_user.email.value,
            created_at=saved_user.created_at.isoformat(),
        )
