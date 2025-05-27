from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl, Field
from .user import UserResponse


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
    id: int
    created_at: datetime
    updated_at: datetime
    user: UserResponse

    class Config:
        orm_mode = True
