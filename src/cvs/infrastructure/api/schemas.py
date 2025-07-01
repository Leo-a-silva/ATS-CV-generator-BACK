from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class Detail(BaseModel):
    message: str


class Data(BaseModel):
    user_id: int
    cv_id: int
    description: Optional[List] = None


class ResponseSchema(BaseModel):
    detail: Detail
    data: Data


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


class CvCreate(BaseModel):
    user_id: int
    cv: CvBase


class WorkExperienceBase(BaseModel):
    role: str
    company_name: str
    summary: str
    start_date: date
    end_date: date


class WorkExperienceCreate(BaseModel):
    cv_id: int
    work_experiences: List[WorkExperienceBase]


class EducationBase(BaseModel):
    title: str
    institution: str
    start_date: date
    end_date: date


class EducationCreate(BaseModel):
    cv_id: int
    educations: List[EducationBase]
