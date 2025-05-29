from dataclasses import dataclass
import phonenumbers
import validators

from cvs.domain.exceptions import (
    InvalidPhoneNumberException,
    InvalidEmailAddressException,
    InvalidUrlException,
)


@dataclass(frozen=True, kw_only=True)
class CvPhoneNumber:
    phone_number: str

    def __post_init__(self) -> None:
        try:
            phonenumbers.parse(self.phone_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise InvalidPhoneNumberException


@dataclass(frozen=True, kw_only=True)
class CvEmailAddress:
    email_address: str

    def __post_init__(self) -> None:
        if not validators.email(self.email_address):
            raise InvalidEmailAddressException


@dataclass(frozen=True, kw_only=True)
class CvURL:
    url: str

    def __post_init__(self) -> None:
        if not validators.url(self.url):
            raise InvalidUrlException
