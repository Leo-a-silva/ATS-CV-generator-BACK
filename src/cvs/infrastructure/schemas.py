from pydantic import BaseModel

from cvs.domain.models import Cv


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
