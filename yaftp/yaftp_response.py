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

class FileStatus(YAFTPResponse):
    def __init__(self, file_status=""):
        super().__init__(213, "File status:\n")
        self.description += file_status

class UserLoggedIn(YAFTPResponse):
    def __init__(self):
        super().__init__(230, "User logged in, proceed. Logged out if appropriate.")

class UserLoggedOut(YAFTPResponse):
    def __init__(self):
        super().__init__(231, "User logged out; service terminated.")

class InvalidUserNameOrPassword(YAFTPResponse):
    def __init__(self):
        super().__init__(430, "Invalid username or password.")

class FileUnAvailable(YAFTPResponse):
    def __init__(self, path=""):
        super().__init__(453, f"Requested action not taken. {path} unavailable (e.g., file not found, no access).")

class InvalidCommandOrArguments(YAFTPResponse):
    def __init__(self):
        super().__init__(501, "Syntax error in command or arguments.")

class NotLoggedIn(YAFTPResponse):
    def __init__(self):
        super().__init__(530, "Not logged in.")

CODE_TO_RESPONSES = {
    212: DirectoryStatus,
    213: FileStatus,
    230: UserLoggedIn,
    231: UserLoggedOut,
    430: InvalidUserNameOrPassword,
    453: FileUnAvailable,
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
        