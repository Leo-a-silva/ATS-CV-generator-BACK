from datetime import datetime
import pytest
from cvs.domain.models import Cv
from cvs.domain.value_objects import CvEmailAddress, CvPhoneNumber, CvURL
from cvs.infrastructure.repositories import SQLModelCvsRepository, CvModel
from shared.infrastructure.db_conf import engine
from sqlmodel import SQLModel, Session, select

from src.users.infrastructure.repositories import UserModel


class TestSQLModelCvRepository:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_saves_cv_to_database(self) -> None:
        repo = SQLModelCvsRepository()

        with Session(engine) as session:
            user = UserModel(
                first_name="Steve",
                last_name="Jobs",
                email_address="steve.jobs@example.com",
                hashed_password="FAKEHASHEDPASSWORD12345!",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            session.add(user)
            session.commit()

        repo.save(
            Cv(
                user_id=1,
                first_name="Steve",
                last_name="Jobs",
                email_address=CvEmailAddress(value="steve.jobs@example.com"),
                phone_number=CvPhoneNumber(value="+543434586789"),
                linkedin_url=CvURL(value="https://linkedin.com/"),
                portfolio_url=CvURL(value="https://ats.com/"),
                country="ARG",
                city="Buenos Aires",
                summary="Co-founder Apple Inc",
            )
        )

        with Session(engine) as session:
            statement = select(CvModel)
            cv = session.exec(statement).first()
            assert cv.summary == "Co-founder Apple Inc"

    def test_returns_all_cvs(self) -> None:
        repo = SQLModelCvsRepository()

        with Session(engine) as session:
            user = UserModel(
                first_name="Steve",
                last_name="Jobs",
                email_address="steve.jobs@example.com",
                hashed_password="FAKEHASHEDPASSWORD12345!",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            session.add(user)
            session.commit()

            cv = CvModel(
                user_id=1,
                first_name="Linus",
                last_name="Torvalds",
                email_address="linus.torvalds@example.com",
                phone_number="+543434586888",
                linkedin_url="https://linkedin.com/",
                portfolio_url="https://ats.com/",
                country="ARG",
                city="Buenos Aires",
                summary="TV Star",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            session.add(cv)
            session.commit()

        cvs = SQLModelCvsRepository().all()

        assert len(cvs) == 1
        assert cvs[0].first_name == "Linus"
