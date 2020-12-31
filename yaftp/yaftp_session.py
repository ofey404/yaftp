from .yaftp_response import YAFTPResponse

class YAFTPSession:
    def __init__(self, local_dir, authenticator=None):
        self.user = None
        self.login = False
        self.work_dir = "/"
        self.auth = authenticator
