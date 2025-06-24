from typing import Optional

from cvs.domain.value_objects import CvEmailAddress, CvPhoneNumber, CvURL, DateObject
from src.shared.domain.value_objects import Id


class Cv:
    def __init__(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        email_address: CvEmailAddress,
        phone_number: CvPhoneNumber,
        linkedin_url: CvURL,
        portfolio_url: CvURL,
        country: str,
        city: str,
        summary: str,
        id: Optional[Id] = None,
    ):
        self._id = id
        self._user_id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._email_address = email_address
        self._phone_number = phone_number
        self._linkedin_url = linkedin_url
        self._portfolio_url = portfolio_url
        self._country = country
        self._city = city
        self._summary = summary

    @classmethod
    def create(
        cls,
        user_id: int,
        first_name: str,
        last_name: str,
        email_address: CvEmailAddress,
        phone_number: CvPhoneNumber,
        linkedin_url: CvURL,
        portfolio_url: CvURL,
        country: str,
        city: str,
        summary: str,
    ) -> "Cv":
        return cls(
            user_id,
            first_name,
            last_name,
            email_address,
            phone_number,
            linkedin_url,
            portfolio_url,
            country,
            city,
            summary,
        )

    @classmethod
    def from_persistence(
        cls,
        id: Id,
        user_id: int,
        first_name: str,
        last_name: str,
        email_address: CvEmailAddress,
        phone_number: CvPhoneNumber,
        linkedin_url: CvURL,
        portfolio_url: CvURL,
        country: str,
        city: str,
        summary: str,
    ) -> "Cv":
        return cls(
            id=id,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            phone_number=phone_number,
            linkedin_url=linkedin_url,
            portfolio_url=portfolio_url,
            country=country,
            city=city,
            summary=summary,
        )

    def get_id(self) -> Optional[Id]:
        return self._id

    def user_id(self) -> int:
        return self._user_id

    def first_name(self) -> str:
        return self._first_name

    def last_name(self) -> str:
        return self._last_name

    def email_address(self) -> CvEmailAddress:
        return self._email_address

    def phone_number(self) -> CvPhoneNumber:
        return self._phone_number

    def linkedin_url(self) -> CvURL:
        return self._linkedin_url

    def portfolio_url(self) -> CvURL:
        return self._portfolio_url

    def country(self) -> str:
        return self._country

    def city(self) -> str:
        return self._city

    def summary(self) -> str:
        return self._summary

    def is_persisted(self) -> bool:
        return self._id is not None

    def _assign_id(self, cv_id: Id) -> None:
        """
        Internal method for assigning IDs when persisting.
        It should only be called from the repository.
        """
        if self._id is not None:
            raise ValueError("Cannot reassign ID to an already persisted cv")
        self._id = cv_id


class WorkExperience:
    def __init__(
        self,
        cv_id: int,
        role: str,
        company_name: str,
        summary: str,
        start_date: DateObject,
        end_date: DateObject,
    ):
        self._cv_id = cv_id
        self._role = role
        self._company_name = company_name
        self._summary = summary
        self._start_date = start_date
        self._end_date = end_date

    @classmethod
    def create(
        cls,
        cv_id: int,
        role: str,
        company_name: str,
        summary: str,
        start_date: DateObject,
        end_date: DateObject,
    ) -> "Cv":
        return cls(
            cv_id,
            role,
            company_name,
            summary,
            start_date,
            end_date,
        )

    def cv_id(self) -> int:
        return self._cv_id

    def role(self) -> str:
        return self._role

    def company_name(self) -> str:
        return self._company_name

    def summary(self) -> str:
        return self._summary

    def start_date(self) -> DateObject:
        return self._start_date

    def end_date(self) -> DateObject:
        return self._end_date


class Education:
    def __init__(
        self,
        cv_id: int,
        title: str,
        institution: str,
        start_date: DateObject,
        end_date: DateObject,
    ):
        self._cv_id = cv_id
        self._title = title
        self._institution = institution
        self._start_date = start_date
        self._end_date = end_date

    @classmethod
    def create(
        cls,
        cv_id: int,
        title: str,
        institution: str,
        start_date: DateObject,
        end_date: DateObject,
    ) -> "Education":
        return cls(
            cv_id,
            title,
            institution,
            start_date,
            end_date,
        )

    def cv_id(self) -> int:
        return self._cv_id

    def title(self) -> str:
        return self._title

    def institution(self) -> str:
        return self._institution

    def start_date(self) -> DateObject:
        return self._start_date

    def end_date(self) -> DateObject:
        return self._end_date
