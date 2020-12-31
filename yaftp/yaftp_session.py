from .yaftp_response import YAFTPResponse

class YAFTPSession:
    def __init__(self, root_dir, authenticator=None):
        self.user = None
        self.login = False
        self.root_dir = root_dir
        self.work_dir = "."
        self.auth = authenticator
        self.ended = False
