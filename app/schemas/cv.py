from pydantic import BaseModel, EmailStr, HttpUrl, Field
from datetime import datetime


class CvBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email_address: EmailStr | None = None
    phone_number: int
    linkedin_url: HttpUrl
    portfolio_url: HttpUrl
    country: str = Field(..., max_length=80)
    city: str = Field(..., max_length=80)
    summary: str


class CvCreate(CvBase):
    user_id: int


class CvResponse(CvBase):
    cv_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
