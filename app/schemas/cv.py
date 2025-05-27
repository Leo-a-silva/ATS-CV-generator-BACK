from pydantic import BaseModel, EmailStr, HttpUrl, Field


class PersonalData(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email_address: EmailStr | None = None
    phone_number: int
    linkedin_url: HttpUrl
    portfolio_url: HttpUrl
    country: str = Field(..., max_length=80)
    city: str = Field(..., max_length=80)
    summary: str
