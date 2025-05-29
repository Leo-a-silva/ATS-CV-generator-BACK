class InvalidPhoneNumberException(Exception):
    def __init__(self, message="Invalid phone number format"):
        self.message = message
        super().__init__(self.message)
