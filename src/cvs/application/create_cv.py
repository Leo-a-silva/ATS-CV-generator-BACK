from dataclasses import dataclass
from cvs.domain.repositories import CvsRepository
from cvs.domain.models import Cv
from cvs.domain.value_objects import CvEmailAddress, CvPhoneNumber, CvURL
from src.cvs.infrastructure.schemas import CvResponse
from src.shared.domain.value_objects import Id
from src.users.domain.exceptions import UserDoesNotExist
from src.users.domain.repositories import UsersRepository


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


@dataclass
class CreateCvResponse:
    cv_id: int
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
    def __init__(
        self,
        cv_repository: CvsRepository,
        users_repository: UsersRepository,
    ):
        self._cv_repository = cv_repository
        self._users_repository = users_repository

    def execute(self, command: CreateCvCommand) -> Cv:
        id_object = Id(value=command.user_id)
        if not self._users_repository.exists_by_id(id_object):
            raise UserDoesNotExist(
                message=f"User with id {command.user_id} does not exist"
            )

        cv_phone_number = CvPhoneNumber(value=command.phone_number)
        cv_email_address = CvEmailAddress(value=command.email_address)
        cv_linkedin_url = CvURL(value=command.linkedin_url)
        cv_portfolio_url = CvURL(value=command.portfolio_url)

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

        saved_cv = self._cv_repository.save(cv)

        return CreateCvResponse(
            cv_id=saved_cv.get_id().value,
            user_id=saved_cv.user_id(),
            first_name=saved_cv.first_name(),
            last_name=saved_cv.last_name(),
            email_address=saved_cv.email_address().value,
            phone_number=saved_cv.phone_number().value,
            linkedin_url=saved_cv.linkedin_url().value,
            portfolio_url=saved_cv.portfolio_url().value,
            country=saved_cv.country(),
            city=saved_cv.city(),
            summary=saved_cv.summary(),
        )
