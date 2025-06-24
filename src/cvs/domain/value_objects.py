from dataclasses import dataclass
import datetime
from typing import Optional
import phonenumbers
import validators

from cvs.domain.exceptions import (
    InvalidDateException,
    InvalidPhoneNumberException,
    InvalidUrlException,
)
from shared.domain.exceptions import InvalidEmailAddressException


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


@dataclass(frozen=True, kw_only=True)
class CvURL:
    value: str

    def __post_init__(self) -> None:
        if not validators.url(self.value):
            raise InvalidUrlException


@dataclass(frozen=True, kw_only=True)
class DateObject:
    value: str
    formatted_value: Optional[datetime.date] = None

    def __post_init__(self) -> None:
        if not self._is_iso8601_date(self.value):
            raise InvalidDateException

        # Save as 'date'
        self.formatted_value = self.value

    @staticmethod
    def _is_iso8601_date(date_str: str) -> bool:
        """Checks if the date has the ISO 8601 date format (“%Y-%m-%d”)"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
