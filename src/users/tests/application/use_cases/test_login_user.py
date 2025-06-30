import pytest
from users.domain.value_objects import InvalidEmailAddressException
from src.users.application.use_cases.login_user import (
    LoginUserCommand,
    LoginUserUseCase,
)
from src.users.domain.exceptions import PasswordDoesNotMatch, UserDoesNotExist
from src.users.infrastructure.repositories import SQLModelUsersRepository
from src.users.infrastructure.services import BcryptPasswordHashingService


class TestCreateCv:
    def test_login_user(self) -> None:
        users_repository = SQLModelUsersRepository()
        password_service = BcryptPasswordHashingService()

        user = LoginUserUseCase(users_repository, password_service).execute(
            LoginUserCommand(
                email_address="steve.jobs@gmail.com",
                password="IloveApples99!",
            )
        )

        assert user.email_address == "steve.jobs@gmail.com"

    def test_login_nonexistent_user(self) -> None:
        users_repository = SQLModelUsersRepository()
        password_service = BcryptPasswordHashingService()

        with pytest.raises(UserDoesNotExist):
            LoginUserUseCase(users_repository, password_service).execute(
                LoginUserCommand(
                    email_address="linus@gmail.com",
                    password="IloveLinux95!",
                )
            )

    def test_login_using_invalid_email(self) -> None:
        users_repository = SQLModelUsersRepository()
        password_service = BcryptPasswordHashingService()

        with pytest.raises(InvalidEmailAddressException):
            LoginUserUseCase(users_repository, password_service).execute(
                LoginUserCommand(
                    email_address="steve",
                    password="IloveApples99!",
                )
            )

    def test_login_using_wrong_password(self) -> None:
        users_repository = SQLModelUsersRepository()
        password_service = BcryptPasswordHashingService()

        with pytest.raises(PasswordDoesNotMatch):
            LoginUserUseCase(users_repository, password_service).execute(
                LoginUserCommand(
                    email_address="steve.jobs@gmail.com",
                    password="IloveWindows98!",
                )
            )
