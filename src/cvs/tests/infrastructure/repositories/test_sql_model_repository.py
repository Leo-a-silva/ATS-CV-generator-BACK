from pytest import Session
from cvs.application.create_cv import CreateCvCommand
from cvs.domain.models import Cv
from cvs.infrastructure.repositories import SQLModelCvsRepository


class TestSQLModelCvRepository:
    def test_saves_cv_to_database(self) -> None:
        repo = SQLModelCvsRepository()

        repo.save(
            Cv(
                user_id=1,
                first_name="John",
                last_name="Doe",
                email_address="john.doe@example.com",
                phone_number="+543434586789",
                linkedin_url="https://linkedin.com/",
                portfolio_url="https://ats.com/",
                country="USA",
                city="New York",
                summary="Software Engineer",
            )
        )

        with Session(engine) as session:
            statement = select(CvModel)
            cv = session.exec(statement).first()
            cv.first_name == "John"
