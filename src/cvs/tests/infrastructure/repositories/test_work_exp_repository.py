import pytest
from cvs.domain.models import WorkExperience
from cvs.infrastructure.repositories import (
    SQLModelWorkExperiencesRepository,
    WorkExperienceModel,
)
from shared.infrastructure.db_conf import engine
from sqlmodel import SQLModel, Session, select


class TestSQLModelWorkExperiencesRepository:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        yield
        SQLModel.metadata.drop_all(engine)

    def test_saves_work_experience_to_database(self) -> None:
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
