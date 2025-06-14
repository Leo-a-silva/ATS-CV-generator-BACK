from cvs.application.create_cv import CreateCv, CreateCvCommand
from cvs.domain.repositories import CvsRepository
from cvs.domain.models import Cv
from cvs.domain.exceptions import (
    InvalidPhoneNumberException,
    InvalidUrlException,
)
from cvs.domain.value_objects import CvEmailAddress, CvPhoneNumber, CvURL
from shared.domain.exceptions import InvalidEmailAddressException


class FakeCvRepository(CvsRepository):
    def __init__(self):
        self._cvs = []

    def save(self, cv: Cv) -> None:
        self._cvs.append(cv)

    def all(self) -> list[Cv]:
        return list(self._cvs)


class TestCreateCv:
    def test_creates_cv_with_all_fields(self) -> None:
        cv_repository = FakeCvRepository()
        CreateCv(cv_repository).execute(
            CreateCvCommand(
                user_id=1,
                first_name="Alex",
                last_name="Caniggia",
                email_address="alex.caniggia@example.com",
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
        assert cv.user_id() == 1
        assert cv.first_name() == "Alex"
        assert cv.last_name() == "Caniggia"
        assert cv.email_address() == CvEmailAddress(value="alex.caniggia@example.com")
        assert cv.phone_number() == CvPhoneNumber(value="+543434586789")
        assert cv.linkedin_url() == CvURL(value="https://linkedin.com/")
        assert cv.portfolio_url() == CvURL(value="https://ats.com/")
        assert cv.country() == "ARG"
        assert cv.city() == "Buenos Aires"
        assert cv.summary() == "Star"

    def test_raise_exception_when_phone_number_is_not_valid(self) -> None:
        cv_repository = FakeCvRepository()
        create_cv_service = CreateCv(cv_repository)

        invalid_phone_command = CreateCvCommand(
            user_id=1,
            first_name="Alex",
            last_name="Caniggia",
            email_address="alex.caniggia@example.com",
            phone_number="3434589536",
            linkedin_url="https://linkedin.com/",
            portfolio_url="https://ats.com/",
            country="ARG",
            city="Buenos Aires",
            summary="Star",
        )
        try:
            create_cv_service.execute(invalid_phone_command)
        except InvalidPhoneNumberException:
            pass
        else:
            assert False, "Expected InvalidPhoneNumberException"

    def test_raise_exception_when_email_is_not_valid(self) -> None:
        cv_repository = FakeCvRepository()
        create_cv_service = CreateCv(cv_repository)

        invalid_email_command = CreateCvCommand(
            user_id=1,
            first_name="Alex",
            last_name="Caniggia",
            email_address="alex.caniggia.example.com",
            phone_number="+543434589536",
            linkedin_url="https://linkedin.com/",
            portfolio_url="https://ats.com/",
            country="ARG",
            city="Buenos Aires",
            summary="Star",
        )
        try:
            create_cv_service.execute(invalid_email_command)
        except InvalidEmailAddressException:
            pass
        else:
            assert False, "Expected InvalidEmailAddressException"

    def test_raise_exception_when_links_are_not_valid(self) -> None:
        cv_repository = FakeCvRepository()
        create_cv_service = CreateCv(cv_repository)

        invalid_links_command = CreateCvCommand(
            user_id=1,
            first_name="Alex",
            last_name="Caniggia",
            email_address="alex.caniggia@example.com",
            phone_number="+543434589536",
            linkedin_url="linkedin-in/mylinkedin",
            portfolio_url="https://ats.com/",
            country="ARG",
            city="Buenos Aires",
            summary="Star",
        )
        try:
            create_cv_service.execute(invalid_links_command)
        except InvalidUrlException:
            pass
        else:
            assert False, "Expected InvalidUrlException"
