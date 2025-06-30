import pytest
from cvs.application.create_cv import CreateCv, CreateCvCommand
from cvs.domain.exceptions import (
    InvalidPhoneNumberException,
    InvalidUrlException,
)
from shared.domain.exceptions import InvalidEmailAddressException
from src.cvs.tests.application.fake_repositories import (
    FakeCvRepository,
    FakeUsersRepository,
)
from src.users.domain.exceptions import UserDoesNotExist
from shared.infrastructure.logger_conf import logger


class TestCreateCv:
    def test_creates_cv_with_all_fields(self) -> None:
        cv_repository = FakeCvRepository()
        users_repository = FakeUsersRepository()

        new_user = {
            "id": 1,
            "first_name": "Steve",
            "last_name": "Jobs",
            "email_address": "steve.jobs@example.com",
            "hashed_password": "MyHashedPassword123",
            "created_at": "2025-06-23 16:45:48",
            "updated_at": "2025-06-23 16:45:48",
        }
        users_repository.save(new_user)

        CreateCv(cv_repository, users_repository).execute(
            CreateCvCommand(
                user_id=1,
                first_name="Steve",
                last_name="Jobs",
                email_address="steve.jobs@example.com",
                phone_number="+543434586789",
                linkedin_url="https://linkedin.com/",
                portfolio_url="https://ats.com/",
                country="ARG",
                city="Buenos Aires",
                summary="Star",
            )
        )

        cvs = cv_repository.all()
        assert len(cvs) == 1
        cv = cvs[0]
        logger.info(cv.email_address())
        assert cv.user_id() == 1
        assert cv.first_name() == "Steve"
        assert cv.last_name() == "Jobs"
        assert cv.email_address().value == "steve.jobs@example.com"
        assert cv.phone_number().value == "+543434586789"
        assert cv.linkedin_url().value == "https://linkedin.com/"
        assert cv.portfolio_url().value == "https://ats.com/"
        assert cv.country() == "ARG"
        assert cv.city() == "Buenos Aires"
        assert cv.summary() == "Star"

    def test_raise_exception_when_phone_number_is_not_valid(self) -> None:
        cv_repository = FakeCvRepository()
        users_repository = FakeUsersRepository()
        create_cv_service = CreateCv(cv_repository, users_repository)

        new_user = {
            "id": 2,
            "first_name": "Steve",
            "last_name": "Jobs",
            "email_address": "steve.jobs@example.com",
            "hashed_password": "MyHashedPassword123",
            "created_at": "2025-06-23 16:45:48",
            "updated_at": "2025-06-23 16:45:48",
        }
        users_repository.save(new_user)

        invalid_phone_command = CreateCvCommand(
            user_id=2,
            first_name="Steve",
            last_name="Jobs",
            email_address="steve.jobs@example.com",
            phone_number="3434589536",
            linkedin_url="https://linkedin.com/",
            portfolio_url="https://ats.com/",
            country="ARG",
            city="Buenos Aires",
            summary="Star",
        )
        with pytest.raises(InvalidPhoneNumberException):
            create_cv_service.execute(invalid_phone_command)

    def test_raise_exception_when_email_is_not_valid(self) -> None:
        cv_repository = FakeCvRepository()
        users_repository = FakeUsersRepository()
        create_cv_service = CreateCv(cv_repository, users_repository)

        new_user = {
            "id": 3,
            "first_name": "Steve",
            "last_name": "Jobs",
            "email_address": "steve.jobs@example.com",
            "hashed_password": "MyHashedPassword123",
            "created_at": "2025-06-23 16:45:48",
            "updated_at": "2025-06-23 16:45:48",
        }
        users_repository.save(new_user)

        invalid_email_command = CreateCvCommand(
            user_id=3,
            first_name="Steve",
            last_name="Jobs",
            email_address="steve.jobs",
            phone_number="+543434589536",
            linkedin_url="https://linkedin.com/",
            portfolio_url="https://ats.com/",
            country="ARG",
            city="Buenos Aires",
            summary="Star",
        )
        with pytest.raises(InvalidEmailAddressException):
            create_cv_service.execute(invalid_email_command)

    def test_raise_exception_when_links_are_not_valid(self) -> None:
        cv_repository = FakeCvRepository()
        users_repository = FakeUsersRepository()
        create_cv_service = CreateCv(cv_repository, users_repository)

        new_user = {
            "id": 4,
            "first_name": "Steve",
            "last_name": "Jobs",
            "email_address": "steve.jobs@example.com",
            "hashed_password": "MyHashedPassword123",
            "created_at": "2025-06-23 16:45:48",
            "updated_at": "2025-06-23 16:45:48",
        }
        users_repository.save(new_user)

        with pytest.raises(InvalidUrlException):
            invalid_links_command = CreateCvCommand(
                user_id=4,
                first_name="Steve",
                last_name="Jobs",
                email_address="steve.jobs@example.com",
                phone_number="+543434589536",
                linkedin_url="linkedin-in/mylinkedin",
                portfolio_url="https://ats.com/",
                country="ARG",
                city="Buenos Aires",
                summary="Star",
            )
            create_cv_service.execute(invalid_links_command)

    def test_raise_exception_when_user_does_not_exists(self) -> None:
        cv_repository = FakeCvRepository()
        users_repository = FakeUsersRepository()
        create_cv_service = CreateCv(cv_repository, users_repository)

        invalid_user_id_command = CreateCvCommand(
            user_id=5,
            first_name="Steve",
            last_name="Jobs",
            email_address="steve.jobs@example.com",
            phone_number="+543434589536",
            linkedin_url="linkedin-in/mylinkedin",
            portfolio_url="https://ats.com/",
            country="ARG",
            city="Buenos Aires",
            summary="Star",
        )
        with pytest.raises(UserDoesNotExist):
            create_cv_service.execute(invalid_user_id_command)
