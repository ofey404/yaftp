class YAFTPResponse:
    def __init__(self, code=None, description=None):
        self.code = code
        self.description = description

    def __str__(self):
        return f"{self.code}: {self.description}"

class UserLoggedIn(YAFTPResponse):
    def __init__(self):
        super().__init__(230, "User logged in, proceed. Logged out if appropriate.")

class InvalidUserNameOrPassword(YAFTPResponse):
    def __init__(self):
        super().__init__(430, "Invalid username or password.")

CODE_TO_RESPONSES = {
    230: UserLoggedIn,
    430: InvalidUserNameOrPassword
}

class YAFTPResponseParser:
    def __init__(self):
        pass

    def parse(self, target) -> YAFTPResponse:
        if isinstance(target, str):
            return self.from_string(target)
            
    def from_string(self, response_string: str) -> YAFTPResponse:
        # TODO: Error handling
        s = response_string.split(": ", 1)
        response_type = CODE_TO_RESPONSES[int(s[0])]
        # FIXIT: Logic problem - only check response code.
        return response_type()
        