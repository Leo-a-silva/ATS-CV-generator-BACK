from cvs.domain.value_objects import CvEmailAddress, CvPhoneNumber


class Cv:
    def __init__(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: str,
        linkedin_url: str,
        portfolio_url: str,
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
        linkedin_url: str,
        portfolio_url: str,
        country: str,
        city: str,
        summary: str,
    ) -> "Cv":
        return cls(
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

    # Métodos para acceder a los atributos
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

    def linkedin_url(self) -> str:
        return self._linkedin_url

    def portfolio_url(self) -> str:
        return self._portfolio_url

    def country(self) -> str:
        return self._country

    def city(self) -> str:
        return self._city

    def summary(self) -> str:
        return self._summary
