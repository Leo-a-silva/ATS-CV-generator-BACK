from dataclasses import dataclass
from cvs.domain.repositories import CvsRepository
from cvs.domain.models import Cv
from cvs.domain.value_objects import CvEmailAddress, CvPhoneNumber, CvURL


@dataclass
class CreateCvCommand:
    user_id: int
    first_name: str
    last_name: str
    email_address: str
    phone_number: str
    linkedin_url: str
    portfolio_url: str
    country: str
    city: str
    summary: str


class CreateCv:
    def __init__(self, cv_repository: CvsRepository):
        self._cv_repository = cv_repository

    def execute(self, command: CreateCvCommand) -> None:
        cv_phone_number = CvPhoneNumber(phone_number=command.phone_number)
        cv_email_address = CvEmailAddress(email_address=command.email_address)
        cv_linkedin_url = CvURL(url=command.linkedin_url)
        cv_portfolio_url = CvURL(url=command.portfolio_url)

        cv = Cv.create(
            user_id=command.user_id,
            first_name=command.first_name,
            last_name=command.last_name,
            email_address=cv_email_address,
            phone_number=cv_phone_number,
            linkedin_url=cv_linkedin_url,
            portfolio_url=cv_portfolio_url,
            country=command.country,
            city=command.city,
            summary=command.summary,
        )

        self._cv_repository.save(cv)
