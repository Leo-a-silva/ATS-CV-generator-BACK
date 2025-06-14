class WeakPasswordException(Exception):
    def __init__(self, message="The password is not secure"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsException(Exception):
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)
