from datetime import datetime
from typing import Optional
from cvs.domain.repositories import (
    CoursesRepository,
    CvsRepository,
    EducationsRepository,
    WorkExperiencesRepository,
    SkillsRepository
)
from cvs.domain.models import Cv, Education, WorkExperience, Skill
from src.cvs.domain.value_objects import CvEmailAddress, CvPhoneNumber, CvURL
from src.shared.domain.value_objects import Id
from src.users.domain.models import User
from src.users.domain.repositories import UsersRepository
from src.users.domain.value_objects import UserEmailAddress


class FakeCourseRepository(CoursesRepository):
    def __init__(self):
        self._courses = []

    def all(self) -> list[Education]:
        return list(self._courses)

    def all_by_cv_id(self, id: Id) -> list[Education]:
        primitive_cv_id = id.value if hasattr(id, "value") else id

        results: list[Education] = [
            course for course in self._courses if (course.cv_id() == primitive_cv_id)
        ]

        return results

    def save(self, work_experience: Education) -> None:
        self._courses.append(work_experience)


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

    
class FakeSkillsRepository(SkillsRepository):
    def __init__(self):
        self._skills = []

    def all_by_cv_id(self, id: Id) -> list[Skill]:
        primitive_cv_id = id.value if hasattr(id, "value") else id

        results: list[Skill] = [
            skill for skill in self._skills if skill.cv_id() == primitive_cv_id
        ]

        return results

    def save(self, skill: Skill) -> None:
        self._skills.append(skill)


class FakeCvRepository(CvsRepository):
    def __init__(self):
        self._cvs = []
        self._next_id = 1

    def save(self, cv: Cv) -> Cv:
        if not cv.is_persisted():
            return self._create_cv(cv)
        else:
            return self._update_cv(cv)

    def all(self) -> list[Cv]:
        return [self._to_domain_model(cv) for cv in self._cvs]

    def exists_by_id(self, id: Id) -> bool:
        primitive_cv_id = id.value if hasattr(id, "value") else id
        return any(cv["id"] == primitive_cv_id for cv in self._cvs)

    def get_by_id(self, id) -> Cv:
        primitive_cv_id = id.value if hasattr(id, "value") else id
        for cv in self._cvs:
            if cv["id"] == primitive_cv_id:
                return self._to_domain_model(cv)

    def _create_cv(self, cv: Cv) -> Cv:
        fake_cv = {
            "id": self._next_id,
            "user_id": cv.user_id(),
            "first_name": cv.first_name(),
            "last_name": cv.last_name(),
            "email_address": cv.email_address().value,
            "phone_number": cv.phone_number().value,
            "linkedin_url": cv.linkedin_url().value,
            "portfolio_url": cv.portfolio_url().value,
            "country": cv.country(),
            "city": cv.city(),
            "summary": cv.summary(),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        self._next_id += 1
        self._cvs.append(fake_cv)
        return self._to_domain_model(fake_cv)

    def _update_cv(self, cv: Cv) -> Cv:
        if not cv.id():
            raise ValueError("Cannot update CV without ID")

        primitive_cv_id = cv.id().value
        for stored_cv in self._cvs:
            if stored_cv["id"] == primitive_cv_id:
                stored_cv.update(
                    {
                        "first_name": cv.first_name(),
                        "last_name": cv.last_name(),
                        "email_address": cv.email_address().value,
                        "phone_number": cv.phone_number().value,
                        "linkedin_url": cv.linkedin_url().value,
                        "portfolio_url": cv.portfolio_url().value,
                        "country": cv.country(),
                        "city": cv.city(),
                        "summary": cv.summary(),
                        "updated_at": datetime.now(),
                    }
                )
                return self._to_domain_model(stored_cv)

        raise ValueError(f"CV with id {primitive_cv_id} not found")

    def _to_domain_model(self, cv_data: dict) -> Cv:
        return Cv.from_persistence(
            id=Id(value=cv_data["id"]),
            user_id=cv_data["user_id"],
            first_name=cv_data["first_name"],
            last_name=cv_data["last_name"],
            email_address=CvEmailAddress(value=cv_data["email_address"]),
            phone_number=CvPhoneNumber(value=cv_data["phone_number"]),
            linkedin_url=CvURL(value=cv_data["linkedin_url"]),
            portfolio_url=CvURL(value=cv_data["portfolio_url"]),
            country=cv_data["country"],
            city=cv_data["city"],
            summary=cv_data["summary"],
        )


class FakeUsersRepository(UsersRepository):
    def __init__(self):
        self._users = []

    def all(self) -> list[User]:
        return list(self._users)

    def save(self, user: User) -> None:
        self._users.append(user)

    def exists_by_id(self, id: Id) -> bool:
        return any(user["id"] == id.value for user in self._users)

    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    def find_by_email(self, email: UserEmailAddress) -> Optional[User]:
        pass

    def exists_by_email(self, email: UserEmailAddress) -> bool:
        pass
