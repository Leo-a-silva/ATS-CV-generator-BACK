from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email_address: EmailStr


class UserCreate(UserBase):
    password_hash: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
