from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email_address: EmailStr


class UserCreate(UserBase):
    password_hash: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
