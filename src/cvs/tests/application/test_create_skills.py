from src.cvs.application.create_cv import CreateCv, CreateCvCommand
from src.cvs.application.create_skills import CreateSkill, CreateSkillCommand
from src.cvs.tests.application.fake_repositories import (
    FakeCvRepository,
    FakeSkillsRepository,
    FakeUsersRepository,
)


class TestCreateSkills:
    def test_creates_skills_with_all_fields(self) -> None:
        cv_repository = FakeCvRepository()
        users_repository = FakeUsersRepository()
        skills_repository = FakeSkillsRepository()

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

        CreateSkill(skills_repository, cv_repository).execute(
            CreateSkillCommand(
                cv_id=1,
                skills=["Python", "Javascript", "React", "FastAPI"],
            )
        )

        skills = skills_repository.all_by_cv_id(id=1)
        assert len(skills) == 1
        skill = skills[0]
        assert skill.get_skills() == ["Python", "Javascript", "React", "FastAPI"]
        assert skill.cv_id() == 1