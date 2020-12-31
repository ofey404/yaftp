class YAFTPResponse:
    def __init__(self, code=None, description=None):
        self.code = code
        self.description = description

    def __str__(self):
        return f"{self.code}: {self.description}"

class DirectoryStatus(YAFTPResponse):
    def __init__(self, dir_status=""):
        super().__init__(212, "Directory status:\n")
        self.description += dir_status

class UserLoggedIn(YAFTPResponse):
    def __init__(self):
        super().__init__(230, "User logged in, proceed. Logged out if appropriate.")

class InvalidUserNameOrPassword(YAFTPResponse):
    def __init__(self):
        super().__init__(430, "Invalid username or password.")

class InvalidCommandOrArguments(YAFTPResponse):
    def __init__(self):
        super().__init__(501, "Syntax error in command or arguments.")

class NotLoggedIn(YAFTPResponse):
    def __init__(self):
        super().__init__(530, "Not logged in.")

CODE_TO_RESPONSES = {
    212: DirectoryStatus,
    230: UserLoggedIn,
    430: InvalidUserNameOrPassword,
    501: InvalidCommandOrArguments,
    530: NotLoggedIn
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
        