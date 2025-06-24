from typing import Optional
from cvs.domain.repositories import (
    CvsRepository,
    EducationsRepository,
    WorkExperiencesRepository,
)
from cvs.domain.models import Cv, Education, WorkExperience
from src.shared.domain.value_objects import Id
from src.users.domain.models import User
from src.users.domain.repositories import UsersRepository
from src.users.domain.value_objects import UserEmailAddress


class FakeEducationRepository(EducationsRepository):
    def __init__(self):
        self._educations = []

    def all(self) -> list[Education]:
        return list(self._educations)

    def all_by_cv_id(self, id: Id) -> list[Education]:
        primitive_cv_id = id.value if hasattr(id, "value") else id

        results: list[Education] = [
            we for we in self._educations if (we.cv_id() == primitive_cv_id)
        ]

        return results

    def save(self, work_experience: Education) -> None:
        self._educations.append(work_experience)


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
