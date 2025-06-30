class WeakPasswordException(Exception):
    def __init__(self, message="The password is not secure"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsException(Exception):
    def __init__(self, message="User with the same email already exists"):
        self.message = message
        super().__init__(self.message)


class UserDoesNotExist(Exception):
    def __init__(self, message="User does not exists"):
        self.message = message
        super().__init__(self.message)


class PasswordDoesNotMatch(Exception):
    def __init__(self, message="The password that you've entered is incorrect."):
        self.message = message
        super().__init__(self.message)
