class InvalidPhoneNumberException(Exception):
    def __init__(self, message="Invalid phone number format"):
        self.message = message
        super().__init__(self.message)


class InvalidUrlException(Exception):
    def __init__(self, message="Invalid URL format"):
        self.message = message
        super().__init__(self.message)


class InvalidDateException(Exception):
    def __init__(
        self,
        message="Invalid date format. The date should follow the ISO 8601 format (“%Y-%m-%d”).",
    ):
        self.message = message
        super().__init__(self.message)
