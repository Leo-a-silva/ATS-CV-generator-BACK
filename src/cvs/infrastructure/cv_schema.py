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
    @classmethod
    def from_domain(cls, cv: Cv) -> "Cv":
        return cls(
            first_name=cv.first_name(),
            last_name=cv.last_name(),
            email_address=cv.email_address().value,
            phone_number=cv.phone_number().value,
            linkedin_url=cv.linkedin_url().value,
            portfolio_url=cv.portfolio_url().value,
            country=cv.country(),
            city=cv.city(),
            summary=cv.summary(),
        )
