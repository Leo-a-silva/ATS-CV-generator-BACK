from datetime import datetime
import pytest
from cvs.domain.models import WorkExperience
from cvs.infrastructure.repositories import (
    SQLModelWorkExperiencesRepository,
    WorkExperienceModel,
    CvModel,
)
from users.infrastructure.repositories import UserModel
from shared.infrastructure.db_conf import engine
from sqlmodel import SQLModel, Session, select


class TestSQLModelWorkExperiencesRepository:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_saves_work_experience_to_database(self) -> None:
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
                phone_number="+543434589536",
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

        repo = SQLModelWorkExperiencesRepository()

        repo.save(
            WorkExperience(
                cv_id=1,
                role="Software Developer",
                company_name="Share IT",
                summary="Designed and implemented a REST API to generate ATS-proof CVs.",
                start_date="2024-06-24",
                end_date="2025-06-24",
            )
        )

        with Session(engine) as session:
            statement = select(WorkExperienceModel)
            work_experience = session.exec(statement).first()
            assert work_experience.company_name == "Share IT"

    def test_get_work_experiences_from_db(self) -> None:
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
                phone_number="+543434589536",
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
                WorkExperienceModel(
                    cv_id=1,
                    role="Dev Ops",
                    company_name="Share IT",
                    summary="Design and implemented CI/CD Pipelines.",
                    start_date="2023-06-24",
                    end_date="2024-06-24",
                )
            )
            session.add(
                WorkExperienceModel(
                    cv_id=1,
                    role="Software Developer",
                    company_name="Share IT",
                    summary="Designed and implemented a REST API to generate ATS-proof CVs.",
                    start_date="2024-06-24",
                    end_date="2025-06-24",
                )
            )
            session.commit()

        work_experiences = SQLModelWorkExperiencesRepository().all_by_cv_id(cv_id=1)

        assert len(work_experiences) == 2
        assert work_experiences[0].role() == "Dev Ops"
