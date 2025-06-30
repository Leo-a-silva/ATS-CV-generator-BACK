from src.cvs.application.create_education import CreateEducation, CreateEducationCommand
from src.cvs.tests.application.fake_repositories import (
    FakeCvRepository,
    FakeEducationRepository,
    FakeUsersRepository,
)


class TestCreateEducation:
    def test_creates_education_with_all_fields(self) -> None:
        cv_repository = FakeCvRepository()
        users_repository = FakeUsersRepository()
        education_repository = FakeEducationRepository()

        new_user = {
            "id": 1,
            "email_address": "steve.jobs@example.com",
            "hashed_password": "MyHashedPassword123",
            "created_at": "2025-06-23 16:45:48",
            "updated_at": "2025-06-23 16:45:48",
        }
        users_repository.save(new_user)

        new_cv = {
            "id": 1,
            "user_id": 1,
            "first_name": "Steve",
            "last_name": "Jobs",
            "email_address": "steve.jobs@example.com",
            "phone_number": "+543434586789",
            "linkedin_url": "https://linkedin.com/",
            "portfolio_url": "https://ats.com/",
            "country": "ARG",
            "city": "Buenos Aires",
            "summary": "Star",
        }
        cv_repository.save(new_cv)

        CreateEducation(education_repository, cv_repository).execute(
            CreateEducationCommand(
                cv_id=1,
                title="CS Degree",
                institution="Hardvard",
                start_date="2018-06-24",
                end_date="2023-06-24",
            )
        )
        CreateEducation(education_repository, cv_repository).execute(
            CreateEducationCommand(
                cv_id=1,
                title="ML Engineering",
                institution="Oxford",
                start_date="2023-06-24",
                end_date="2024-06-24",
            )
        )

        educations = education_repository.all_by_cv_id(id=1)
        assert len(educations) == 2
        we = educations[0]
        assert we.title() == "CS Degree"
        assert we.cv_id() == 1
