from .yaftp_response import YAFTPResponse
import os

class YAFTPSession:
    def __init__(self, root_dir, authenticator=None, client_address=None):
        self.user = None
        self.login = False
        self.root_dir = os.path.abspath(root_dir)
        self.work_dir = self.root_dir
        self.auth = authenticator
        self.client_address = client_address
        self.ended = False
