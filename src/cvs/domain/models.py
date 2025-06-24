from cvs.domain.value_objects import CvEmailAddress, CvPhoneNumber, CvURL, DateObject


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
    ):
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

    def start_date(self) -> DateObject:
        return self._start_date

    def end_date(self) -> DateObject:
        return self._end_date

    def summary(self) -> str:
        return self._summary
