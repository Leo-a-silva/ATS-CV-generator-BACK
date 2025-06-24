from datetime import datetime
import pytest
from cvs.domain.models import Education
from cvs.infrastructure.repositories import (
    EducationModel,
    SQLModelEducationsRepository,
    CvModel,
)
from users.infrastructure.repositories import UserModel
from shared.infrastructure.db_conf import engine
from sqlmodel import SQLModel, Session, select


class TestSQLModelEducationsRepository:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_saves_education_to_database(self) -> None:
        # Fake user and cv
        with Session(engine) as session:
            user = UserModel(
                email_address="alex@example.com",
                hashed_password="FAKEHASHEDPASSWORD12345!",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            cv = CvModel(
                id=1,
                user_id=1,
                first_name="Alex",
                last_name="Caniggia",
                email_address="alex@example.com",
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

        repo = SQLModelEducationsRepository()

        repo.save(
            Education(
                cv_id=1,
                title="CS Degree",
                institution="Hardvard",
                start_date="2018-06-24",
                end_date="2023-06-24",
            )
        )

        with Session(engine) as session:
            statement = select(EducationModel)
            education = session.exec(statement).first()
            assert education.institution == "Hardvard"

    def test_get_educations_from_db(self) -> None:
        with Session(engine) as session:
            user = UserModel(
                email_address="alex@example.com",
                hashed_password="FAKEHASHEDPASSWORD12345!",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            cv = CvModel(
                id=1,
                user_id=1,
                first_name="Alex",
                last_name="Caniggia",
                email_address="alex@example.com",
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
                EducationModel(
                    cv_id=1,
                    title="CS Degree",
                    institution="Hardvard",
                    start_date="2018-06-24",
                    end_date="2023-06-24",
                )
            )
            session.add(
                EducationModel(
                    cv_id=1,
                    title="ML Engineering",
                    institution="Oxford",
                    start_date="2023-06-24",
                    end_date="2024-06-24",
                )
            )
            session.commit()

        work_experiences = SQLModelEducationsRepository().all_by_cv_id(cv_id=1)

        assert len(work_experiences) == 2
        assert work_experiences[0].title() == "CS Degree"
