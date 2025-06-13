class InvalidEmailAddressException(Exception):
    def __init__(self, message="Invalid email address format"):
        self.message = message
        super().__init__(self.message)
