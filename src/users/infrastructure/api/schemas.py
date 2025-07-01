from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class Detail(BaseModel):
    message: str


class Data(BaseModel):
    user_id: int
    access_token: Optional[str] = None
    description: Optional[List] = None


class ResponseSchema(BaseModel):
    detail: Detail
    data: Data


class RegisterUserRequest(BaseModel):
    first_name: str
    last_name: str
    email_address: EmailStr
    password: str


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email_address: str
    created_at: datetime


class LoginUserRequest(BaseModel):
    email_address: EmailStr
    password: str
