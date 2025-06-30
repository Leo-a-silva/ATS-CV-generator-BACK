from cvs.application.create_work_experience import CreateWorkExperience, CreateWECommand
from src.cvs.tests.application.fake_repositories import (
    FakeCvRepository,
    FakeUsersRepository,
    FakeWorkExperienceRepository,
)


class TestCreateWorkExperience:
    def test_creates_work_experience_with_all_fields(self) -> None:
        cv_repository = FakeCvRepository()
        users_repository = FakeUsersRepository()
        work_experience_repository = FakeWorkExperienceRepository()

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

        CreateWorkExperience(work_experience_repository, cv_repository).execute(
            CreateWECommand(
                cv_id=1,
                role="Software Developer",
                company_name="Share IT",
                summary="Designed and implemented a REST API to generate ATS-proof CVs.",
                start_date="2024-06-24",
                end_date="2024-06-24",
            )
        )
        CreateWorkExperience(work_experience_repository, cv_repository).execute(
            CreateWECommand(
                cv_id=1,
                role="Dev Ops",
                company_name="Share IT",
                summary="Design and implemented CI/CD Pipelines.",
                start_date="2023-06-24",
                end_date="2024-06-24",
            )
        )

        work_experiences = work_experience_repository.all_by_cv_id(id=1)
        assert len(work_experiences) == 2
        we = work_experiences[0]
        assert we.role() == "Software Developer"
        assert we.cv_id() == 1
