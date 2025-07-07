from datetime import datetime
import pytest
from cvs.domain.models import Course
from cvs.infrastructure.repositories import (
    CoursesModel,
    SQLModelCoursesRepository,
    CvModel,
)
from users.infrastructure.repositories import UserModel
from shared.infrastructure.db_conf import engine
from sqlmodel import SQLModel, Session, select


class TestSQLModelCoursesRepository:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_saves_course_to_database(self) -> None:
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

        repo = SQLModelCoursesRepository()

        repo.save(
            Course(
                cv_id=1,
                title="CS50 Machine Learning with Python",
                institution="Hardvard",
                start_date="2022-09-28",
            )
        )

        with Session(engine) as session:
            statement = select(CoursesModel)
            education = session.exec(statement).first()
            assert education.title == "CS50 Machine Learning with Python"

    def test_get_courses_from_db(self) -> None:
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
                CoursesModel(
                    cv_id=1,
                    title="CS50 Machine Learning with Python",
                    institution="Hardvard",
                    start_date="2022-09-28",
                )
            )
            session.add(
                CoursesModel(
                    cv_id=1,
                    title="AWS Cloud Practitioner",
                    institution="Udemy",
                    start_date="2024-03-18",
                )
            )
            session.commit()

        courses = SQLModelCoursesRepository().all_by_cv_id(cv_id=1)

        assert len(courses) == 2
        assert courses[0].title() == "CS50 Machine Learning with Python"
