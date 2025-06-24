from datetime import date, datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, Session, select

from src.cvs.domain.value_objects import CvEmailAddress, CvPhoneNumber, CvURL
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
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    work_experiences: List["WorkExperienceModel"] = Relationship(back_populates="cv")
    studies: List["EducationModel"] = Relationship(back_populates="cv")
    courses: List["CoursesModel"] = Relationship(back_populates="cv")
    skills: List["SkillsModel"] = Relationship(back_populates="cv")


class WorkExperienceModel(SQLModel, table=True):
    __tablename__ = "work_experiences"

    id: int | None = Field(default=None, primary_key=True)
    cv_id: int | None = Field(default=None, foreign_key="cvs.id")
    cv: Optional["CvModel"] = Relationship(back_populates="work_experiences")

    role: str = Field(..., max_length=80)
    company_name: str = Field(..., max_length=100)
    summary: str = Field(..., max_length=100)
    start_date: date
    end_date: Optional[date] = None


class EducationModel(SQLModel, table=True):
    __tablename__ = "studies"

    id: int | None = Field(default=None, primary_key=True)
    cv_id: int | None = Field(default=None, foreign_key="cvs.id")
    cv: Optional["CvModel"] = Relationship(back_populates="studies")

    title: str = Field(..., max_length=80)
    institution: str = Field(..., max_length=80)
    start_date: date
    end_date: Optional[date] = None


class CoursesModel(SQLModel, table=True):
    __tablename__ = "courses"

    id: int | None = Field(default=None, primary_key=True)
    cv_id: int | None = Field(default=None, foreign_key="cvs.id")
    cv: Optional["CvModel"] = Relationship(back_populates="courses")

    title: str = Field(..., max_length=80)
    institution: str = Field(..., max_length=80)
    date: date


class SkillsModel(SQLModel, table=True):
    __tablename__ = "skills"

    id: int | None = Field(default=None, primary_key=True)
    cv_id: int | None = Field(default=None, foreign_key="cvs.id")
    cv: Optional["CvModel"] = Relationship(back_populates="skills")

    title: str = Field(..., max_length=30)


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
        if not cv.is_persisted():
            return self._create_cv(cv)
        else:
            return self._update_cv(cv)

    def _create_cv(self, cv: Cv) -> Cv:
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
            session.refresh(cv_model)

        return self._to_domain_model(cv_model)

    def _update_cv(self, cv: Cv) -> Cv:
        if not cv.id():
            raise ValueError("Cannot update CV without ID")

        with Session(engine) as session:
            cv_model = session.get(CvModel, cv.id().value)
            if not cv_model:
                raise ValueError(f"CV with id {cv.id().value} not found")

            cv_model.last_name = (cv.last_name(),)
            cv_model.first_name = (cv.first_name(),)
            cv_model.email_address = (cv.email_address().value,)
            cv_model.phone_number = (cv.phone_number().value,)
            cv_model.linkedin_url = (cv.linkedin_url().value,)
            cv_model.portfolio_url = (cv.portfolio_url().value,)
            cv_model.country = (cv.country(),)
            cv_model.city = (cv.city(),)
            cv_model.summary = (cv.summary(),)
            cv_model.updated_at = cv.updated_at()

            session.commit()
            session.refresh(cv_model)

        return self._to_domain_model(cv_model)

    def _to_domain_model(self, cv_model: CvModel) -> Cv:
        return Cv.from_persistence(
            id=Id(value=cv_model.id),
            user_id=cv_model.user_id,
            first_name=cv_model.first_name,
            last_name=cv_model.last_name,
            email_address=CvEmailAddress(value=cv_model.email_address),
            phone_number=CvPhoneNumber(value=cv_model.phone_number),
            linkedin_url=CvURL(value=cv_model.linkedin_url),
            portfolio_url=CvURL(value=cv_model.portfolio_url),
            country=cv_model.country,
            city=cv_model.city,
            summary=cv_model.summary,
        )


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
            session.refresh(work_experience_model)
