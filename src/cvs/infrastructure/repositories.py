from pydantic import EmailStr
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session
from ..domain.repositories import CvsRepository
from ..domain.models import Cv


class CvModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email_address: EmailStr | None = None
    phone_number: str
    linkedin_url: str
    portfolio_url: str
    country: str = Field(..., max_length=80)
    city: str = Field(..., max_length=80)
    summary: str
    created_at: datetime
    updated_at: datetime


engine = create_engine("sqlite:///database.db", echo=True)
SQLModel.metadata.create_all(engine)


class SQLModelCvsRepository(CvsRepository):
    def all(self) -> list[Cv]:
        pass

    def save(self, cv: Cv) -> None:
        cv_model = CvModel(
            user_id=cv.user_id(),
            first_name=cv.first_name(),
            last_name=cv.last_name(),
            email_address=cv.email_address(),
            phone_number=cv.phone_number(),
            linkedin_url=cv.linkedin_url(),
            portfolio_url=cv.portfolio_url(),
            country=cv.country(),
            city=cv.city(),
            summary=cv.summary(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        with Session(engine) as session:
            session.add(cv_model)
            session.commit()
