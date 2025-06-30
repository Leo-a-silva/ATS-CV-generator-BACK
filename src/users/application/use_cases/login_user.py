from dataclasses import dataclass
import datetime

from ...domain.repositories import UsersRepository
from ...domain.services import PasswordHashingService, TokenService
from ...domain.value_objects import UserEmailAddress
from ...domain.exceptions import (
    PasswordDoesNotMatch,
    UserDoesNotExist,
)


@dataclass
class LoginUserCommand:
    email_address: str
    password: str


@dataclass
class LoginUserResponse:
    user_id: int
    first_name: str
    last_name: str
    email_address: str
    created_at: datetime
    access_token: str


class LoginUserUseCase:
    def __init__(
        self,
        users_repository: UsersRepository,
        password_hashing_service: PasswordHashingService,
        token_service: TokenService,
    ):
        self._users_repository = users_repository
        self._password_hashing_service = password_hashing_service
        self._token_service = token_service

    def execute(self, command: LoginUserCommand) -> LoginUserResponse:
        email_address = UserEmailAddress(value=command.email_address)

        if self._users_repository.exists_by_email(email_address):
            user = self._users_repository.find_by_email(email_address)

            if user is not None:
                user_hashed_password = user.hashed_password()
                if not self._password_hashing_service.verify_password(
                    plain_password=command.password,
                    hashed_password=user_hashed_password,
                ):
                    raise PasswordDoesNotMatch

                access_token = self._token_service.create_access_token(
                    user_id=user.get_id().value
                )
                return LoginUserResponse(
                    user_id=user.get_id().value,
                    first_name=user.first_name(),
                    last_name=user.last_name(),
                    email_address=user.email_address().value,
                    created_at=user.created_at(),
                    access_token=access_token,
                )

        else:
            raise UserDoesNotExist(
                f"User with email {email_address.value} does not exists."
            )
