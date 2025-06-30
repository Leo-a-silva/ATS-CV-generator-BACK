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
