from datetime import datetime
from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    first_name: str
    last_name: str
    email_address: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email_address: str
    created_at: datetime


class LoginResponse(UserResponse):
    access_token: str


class LoginUserRequest(BaseModel):
    email_address: EmailStr
    password: str
