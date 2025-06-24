from datetime import date, datetime
from sqlmodel import Field, SQLModel, Session, select

from src.shared.domain.value_objects import Id

from ..domain.repositories import CvsRepository, WorkExperiencesRepository
from ..domain.models import Cv, WorkExperience

from shared.infrastructure.db_conf import engine


class CvModel(SQLModel, table=True):
    __tablename__ = "cvs"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id")
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
        with Session(engine) as session:
            session.add(cv_model)
            session.commit()


class WorkExperienceModel(SQLModel, table=True):
    __tablename__ = "work_experiences"

    id: int | None = Field(default=None, primary_key=True)
    cv_id: int | None = Field(default=None, foreign_key="cvs.id")
    role: str = Field(..., max_length=80)
    company_name: str = Field(..., max_length=100)
    summary: str = Field(..., max_length=100)
    start_date: date
    end_date: date


class SQLModelWorkExperiencesRepository(WorkExperiencesRepository):
    def all_by_cv_id(self, cv_id: Id) -> list[WorkExperience]:
        with Session(engine) as session:
            work_experiences = session.exec(select(WorkExperienceModel)).filter(
                cv_id=cv_id
            )

            return [
                WorkExperienceModel(
                    id=work_experience.id,
                    role=work_experience.role,
                    company_name=work_experience.company_name,
                    summary=work_experience.summary,
                    start_date=work_experience.start_date,
                    end_date=work_experience.end_date,
                )
                for work_experience in work_experiences
            ]

    def save(self, work_experience: WorkExperience) -> None:
        work_experience_model = WorkExperienceModel(
            cv_id=work_experience.cv_id(),
            role=work_experience.role(),
            company_name=work_experience.company_name(),
            summary=work_experience.summary(),
            start_date=work_experience.start_date(),
            end_date=work_experience.end_date(),
        )
        with Session(engine) as session:
            session.add(work_experience_model)
            session.commit()


class EducationModel(SQLModel, table=True):
    __tablename__ = "studies"

    id: int | None = Field(default=None, primary_key=True)
    cv_id: int | None = Field(default=None, foreign_key="cvs.id")
    title: str = Field(..., max_length=80)
    institution: str = Field(..., max_length=80)
    start_date: date
    end_date: date


class CoursesModel(SQLModel, table=True):
    __tablename__ = "courses"

    id: int | None = Field(default=None, primary_key=True)
    cv_id: int | None = Field(default=None, foreign_key="cvs.id")
    title: str = Field(..., max_length=80)
    institution: str = Field(..., max_length=80)
    date: date


class Skills(SQLModel, table=True):
    __tablename__ = "skills"

    id: int | None = Field(default=None, primary_key=True)
    cv_id: int | None = Field(default=None, foreign_key="cvs.id")
    title: str = Field(..., max_length=30)
