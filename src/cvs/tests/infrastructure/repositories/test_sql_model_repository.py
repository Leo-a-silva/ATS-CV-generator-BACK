import pytest
from cvs.domain.models import Cv
from cvs.infrastructure.repositories import SQLModelCvsRepository, engine, CvModel
from sqlmodel import SQLModel, Session, select


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
            assert cv.first_name == "Alex"

    def test_returns_all_cvs(self) -> None:
        with Session(engine) as session:
            session.add(
                CvModel(
                    user_id=2,
                    first_name="Marcelo",
                    last_name="Tinelli",
                    email_address="marcelo.tinelli@example.com",
                    phone_number="+543434586888",
                    linkedin_url="https://linkedin.com/",
                    portfolio_url="https://ats.com/",
                    country="ARG",
                    city="Buenos Aires",
                    summary="TV Star",
                )
            )
            session.commit()

        cvs = SQLModelCvsRepository().all()

        assert len(cvs) == 1
        assert cvs[0] == CvModel(
            user_id=2,
            first_name="Marcelo",
            last_name="Tinelli",
            email_address="marcelo.tinelli@example.com",
            phone_number="+543434586888",
            linkedin_url="https://linkedin.com/",
            portfolio_url="https://ats.com/",
            country="ARG",
            city="Buenos Aires",
            summary="TV Star",
        )
