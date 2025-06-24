from typing import Optional
from cvs.application.create_work_experience import CreateWorkExperience, CreateWECommand
from cvs.domain.repositories import CvsRepository, WorkExperiencesRepository
from cvs.domain.models import Cv, WorkExperience
from src.shared.domain.value_objects import Id
from src.users.domain.models import User
from src.users.domain.repositories import UsersRepository
from src.users.domain.value_objects import UserEmailAddress


class FakeWorkExperienceRepository(WorkExperiencesRepository):
    def __init__(self):
        self._work_experiences = []

    def all(self) -> list[WorkExperience]:
        return list(self._work_experiences)

    def all_by_cv_id(self, id: Id) -> list[WorkExperience]:
        primitive_cv_id = id.value if hasattr(id, "value") else id

        results: list[WorkExperience] = [
            we for we in self._work_experiences if (we.cv_id() == primitive_cv_id)
        ]

        return results

    def save(self, work_experience: WorkExperience) -> None:
        self._work_experiences.append(work_experience)


class FakeCvRepository(CvsRepository):
    def __init__(self):
        self._cvs = []

    def save(self, cv: Cv) -> None:
        self._cvs.append(cv)

    def all(self) -> list[Cv]:
        return list(self._cvs)

    def exists_by_id(self, id: Id) -> bool:
        primitive_cv_id = id.value if hasattr(id, "value") else id
        return any(cv["id"] == primitive_cv_id for cv in self._cvs)


class FakeUsersRepository(UsersRepository):
    def __init__(self):
        self._users = []

    def all(self) -> list[User]:
        return list(self._users)

    def save(self, user: User) -> None:
        self._users.append(user)

    def exists_by_id(self, id: Id) -> bool:
        return any(user.id == id for user in self._users)

    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    def find_by_email(self, email: UserEmailAddress) -> Optional[User]:
        pass

    def exists_by_email(self, email: UserEmailAddress) -> bool:
        pass


class TestCreateWorkExperience:
    def test_creates_work_experience_with_all_fields(self) -> None:
        cv_repository = FakeCvRepository()
        users_repository = FakeUsersRepository()
        work_experience_repository = FakeWorkExperienceRepository()

        new_user = {
            "id": 1,
            "email_address": "alex.caniggia@example.com",
            "hashed_password": "MyHashedPassword123",
            "created_at": "2025-06-23 16:45:48",
            "updated_at": "2025-06-23 16:45:48",
        }
        users_repository.save(new_user)

        new_cv = {
            "id": 1,
            "user_id": 1,
            "first_name": "Alex",
            "last_name": "Caniggia",
            "email_address": "alex.caniggia@example.com",
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
