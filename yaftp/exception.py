class YAFTPBaseError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "{} has been raised".format(self.__class__.__name__)

class LoginFailedError(YAFTPBaseError):
    pass

class ParseRequestError(YAFTPBaseError):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        if self.message != None:
            return f"Can't parse request: {self.message}"
        else:
            return "Can't parse request."

class PathOverRootError(YAFTPBaseError):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        if self.message != None:
            return f"Path over root: {self.message}"
        else:
            return "Path over root."