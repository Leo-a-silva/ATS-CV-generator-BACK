from datetime import datetime
from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    email_address: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: int
    email_address: str
    created_at: datetime
