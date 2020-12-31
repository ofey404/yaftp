from .exception import ParseRequestError
from .yaftp_session import YAFTPSession
from .yaftp_response import YAFTPResponse, InvalidUserNameOrPassword, UserLoggedIn, NotLoggedIn, DirectoryStatus
import logging
import os

class YAFTPRequest:
    def __init__(self, name, raw_args=None, accepted_argc=(0,)):
        self.name = name
        self.raw_args = []
        if len(raw_args) not in accepted_argc:
            raise ParseRequestError(f"wrong argument number: {len(raw_args)}")

    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        raise NotImplementedError

class YAFTPLogin(YAFTPRequest):
    def __init__(self, raw_args=None):
        super().__init__("LOGIN", raw_args, accepted_argc=(1,))
        self.username = None
        self.passwd = None
        auth = raw_args[0].split(":")
        if len(auth) == 1:
            self.username = auth[0]
        elif len(auth) == 2:
            self.username = auth[0]
            self.passwd = auth[1]
        else:
            raise ParseRequestError(f"can't parse {raw_args[0]} to valid auth info.")
    
    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        if (self.username not in session.auth.keys()) or (self.passwd != session.auth[self.username]):
            logging.info(f"invalid username or password: {self.username}:{self.passwd}")
            return InvalidUserNameOrPassword()
        session.user = self.username
        session.login = True
        logging.info(f"user {self.username} logged in")
        return UserLoggedIn()

class YAFTPDir(YAFTPRequest):
    def __init__(self, raw_args=None):
        super().__init__("DIR", raw_args, accepted_argc=(0, 1))
        self.dir = "."
        if len(raw_args) != 0:
            self.dir = raw_args[0]
    
    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        if not session.login:
            logging.info(f"try {self.name} without login")
            return NotLoggedIn()
        path = os.path.join(session.root_dir, session.work_dir, self.dir)
        logging.info(f"execute {self.name} on {path}")
        _, dirs, filenames = next(os.walk(path))
        dirs = list(map(lambda x: x + "/", dirs))
        return DirectoryStatus(dir_status="\n".join(dirs + filenames))

class YAFTPPwd(YAFTPRequest):
    def __init__(self, raw_args=None):
        super().__init__("PWD", raw_args)

class YAFTPGet(YAFTPRequest):
    def __init__(self, raw_args=None):
        super().__init__("GET", raw_args)

class YAFTPSend(YAFTPRequest):
    def __init__(self, raw_args=None):
        super().__init__("SEND", raw_args)

class YAFTPBye(YAFTPRequest):
    def __init__(self, raw_args=None):
        super().__init__("BYE", raw_args)

REQUESTS = {
    "LOGIN": YAFTPLogin,
    "DIR": YAFTPDir,
    "PWD": YAFTPPwd,
    "GET": YAFTPGet,
    "SEND": YAFTPSend,
    "BYE": YAFTPBye
}

class YAFTPRequestParser:
    def __init__(self):
        pass

    def parse(self, target) -> YAFTPRequest:
        if isinstance(target, str):
            return self.from_string(target)

    def from_string(self, request_string: str) -> YAFTPRequest:
        s = request_string.split()
        case_insensitive_command = s[0].upper()
        if len(s) >= 1 and case_insensitive_command in REQUESTS.keys():
            request_type = REQUESTS[case_insensitive_command]
            return request_type(s[1:])
        else:
            raise ParseRequestError(request_string)
