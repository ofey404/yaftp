
class YAFTPBaseError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "{} has been raised".format(self.__class__.__name__)

class LoginFailedError(YAFTPBaseError):
    pass