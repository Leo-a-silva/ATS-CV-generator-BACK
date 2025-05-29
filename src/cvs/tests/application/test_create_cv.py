from cvs.application.create_cv import CreateCv, CreateCvCommand
from cvs.domain.repositories import CvsRepository
from cvs.domain.models import Cv


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
                first_name="John",
                last_name="Doe",
                email_address="john.doe@example.com",
                phone_number=1234567890,
                linkedin_url="https://linkedin.com/in/johndoe",
                portfolio_url="https://johndoe.com",
                country="USA",
                city="New York",
                summary="Software Engineer",
            )
        )

        cvs = cv_repository.all()
        assert len(cvs) == 1
        cv = cvs[0]
        assert cv.user_id() == 1
        assert cv.first_name() == "John"
        assert cv.last_name() == "Doe"
        assert cv.email_address() == "john.doe@example.com"
        assert cv.phone_number() == 1234567890
        assert cv.linkedin_url() == "https://linkedin.com/in/johndoe"
        assert cv.portfolio_url() == "https://johndoe.com"
        assert cv.country() == "USA"
        assert cv.city() == "New York"
        assert cv.summary() == "Software Engineer"
