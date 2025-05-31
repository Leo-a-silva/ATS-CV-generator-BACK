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
    value: str

    def __post_init__(self) -> None:
        try:
            phonenumbers.parse(self.value)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise InvalidPhoneNumberException


@dataclass(frozen=True, kw_only=True)
class CvEmailAddress:
    value: str

    def __post_init__(self) -> None:
        if not validators.email(self.value):
            raise InvalidEmailAddressException

    @property
    def get_value(self) -> str:
        return self._email_address


@dataclass(frozen=True, kw_only=True)
class CvURL:
    value: str

    def __post_init__(self) -> None:
        if not validators.url(self.value):
            raise InvalidUrlException
