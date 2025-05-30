import pytest
from cvs.domain.models import Cv
from cvs.infrastructure.repositories import SQLModelCvsRepository, engine, CvModel
from sqlmodel import SQLModel, Session, select
from shared.infrastructure.logger_conf import logger


class TestSQLModelCvRepository:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        yield
        SQLModel.metadata.drop_all(engine)

    def test_saves_cv_to_database(self) -> None:
        repo = SQLModelCvsRepository()

        repo.save(
            Cv(
                user_id=1,
                first_name="Alex",
                last_name="Caniggia",
                email_address="alex.caniggia@example.com",
                phone_number="+543434586789",
                linkedin_url="https://linkedin.com/",
                portfolio_url="https://ats.com/",
                country="ARG",
                city="Buenos Aires",
                summary="Star",
            )
        )

        with Session(engine) as session:
            statement = select(CvModel)
            cv = session.exec(statement).first()
            logger.info(f"cv: {cv}")
            cv.first_name == "John"
