from datetime import datetime
from sqlmodel import Field, SQLModel, Session, select

from ..domain.repositories import CvsRepository
from ..domain.models import Cv
from shared.infrastructure.logger_conf import logger

from .db_conf import engine


class CvModel(SQLModel, table=True):
    __tablename__ = "Cv"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email_address: str
    phone_number: str
    linkedin_url: str
    portfolio_url: str
    country: str = Field(..., max_length=80)
    city: str = Field(..., max_length=80)
    summary: str
    created_at: datetime
    updated_at: datetime


class SQLModelCvsRepository(CvsRepository):
    def all(self) -> list[Cv]:
        with Session(engine) as session:
            cv_models = session.exec(select(CvModel)).all()

        return [
            CvModel(
                user_id=cv_model.user_id,
                first_name=cv_model.first_name,
                last_name=cv_model.last_name,
                email_address=cv_model.email_address,
                phone_number=cv_model.phone_number,
                linkedin_url=cv_model.linkedin_url,
                portfolio_url=cv_model.portfolio_url,
                country=cv_model.country,
                city=cv_model.city,
                summary=cv_model.summary,
                created_at=cv_model.created_at,
                updated_at=cv_model.updated_at,
            )
            for cv_model in cv_models
        ]

    def save(self, cv: Cv) -> None:
        cv_model = CvModel(
            user_id=cv.user_id(),
            first_name=cv.first_name(),
            last_name=cv.last_name(),
            email_address=cv.email_address().value,
            phone_number=cv.phone_number().value,
            linkedin_url=cv.linkedin_url().value,
            portfolio_url=cv.portfolio_url().value,
            country=cv.country(),
            city=cv.city(),
            summary=cv.summary(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        logger.info({"cv": cv_model})
        with Session(engine) as session:
            session.add(cv_model)
            session.commit()
