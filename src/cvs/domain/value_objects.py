from dataclasses import dataclass
import phonenumbers

from cvs.domain.exceptions import InvalidPhoneNumberException


@dataclass(frozen=True, kw_only=True)
class CvPhoneNumber:
    phone_number: str

    def __post_init__(self) -> None:
        try:
            phonenumbers.parse(self.phone_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise InvalidPhoneNumberException
