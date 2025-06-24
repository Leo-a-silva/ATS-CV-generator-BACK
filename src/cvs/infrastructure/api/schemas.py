from datetime import date
from pydantic import BaseModel


class CvBase(BaseModel):
    first_name: str
    last_name: str
    email_address: str
    phone_number: str
    linkedin_url: str
    portfolio_url: str
    country: str
    city: str
    summary: str


class CvCreate(CvBase):
    user_id: int


class CvResponse(CvBase):
    cv_id: int
    user_id: int
    first_name: str
    last_name: str
    email_address: str
    phone_number: str
    linkedin_url: str
    portfolio_url: str
    country: str
    city: str
    summary: str


class WorkExperienceBase(BaseModel):
    role: str
    company_name: str
    summary: str
    start_date: date
    end_date: date


class WorkExperienceCreate(WorkExperienceBase):
    cv_id: int


class WorkExperienceResponse(WorkExperienceBase):
    pass


class EducationBase(BaseModel):
    title: str
    institution: str
    start_date: date
    end_date: date


class EducationCreate(EducationBase):
    cv_id: int


class EducationResponse(EducationBase):
    pass
