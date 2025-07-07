from datetime import datetime
import pytest
from cvs.domain.models import Skill
from cvs.infrastructure.repositories import (
    SQLModelSkillsRepository,
    SkillsModel,
    CvModel,
)
from users.infrastructure.repositories import UserModel
from shared.infrastructure.db_conf import engine
from sqlmodel import SQLModel, Session, select

import json


class TestSQLModelSkillsRepository:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_saves_skills_to_database(self) -> None:
        # Fake user and cv
        with Session(engine) as session:
            user = UserModel(
                first_name="Steve",
                last_name="Jobs",
                email_address="steve.jobs@example.com",
                hashed_password="FAKEHASHEDPASSWORD12345!",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            cv = CvModel(
                id=1,
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
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            session.add(user)
            session.commit()
            session.add(cv)
            session.commit()

        repo = SQLModelSkillsRepository()

        repo.save(
            Skill(
                cv_id=1,
                skills=["Python", "Javascript", "React", "FastAPI"],
            )
        )

        with Session(engine) as session:
            statement = select(SkillsModel)
            skills_model = session.exec(statement).first()
            assert json.loads(skills_model.skills) == ["Python", "Javascript", "React", "FastAPI"]

    def test_get_skills_from_db(self) -> None:
        with Session(engine) as session:
            user = UserModel(
                first_name="Steve",
                last_name="Jobs",
                email_address="steve.jobs@example.com",
                hashed_password="FAKEHASHEDPASSWORD12345!",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            cv = CvModel(
                id=1,
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
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            session.add(user)
            session.commit()
            session.add(cv)
            session.commit()

            session.add(
                SkillsModel(
                    cv_id=1,
                    skills=json.dumps(["Python", "Javascript", "React", "FastAPI"]),
                )
            )
            session.commit()

        skills = SQLModelSkillsRepository().all_by_cv_id(cv_id=1)

        assert len(skills) == 1
        assert skills[0].get_skills() == ["Python", "Javascript", "React", "FastAPI"]
