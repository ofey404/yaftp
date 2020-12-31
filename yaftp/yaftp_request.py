from .exception import ParseRequestError, PathOverRootError
from .yaftp_session import YAFTPSession
from .yaftp_response import YAFTPResponse, InvalidUserNameOrPassword, UserLoggedIn, NotLoggedIn, DirectoryStatus, FileUnAvailable
import logging
import os

class YAFTPRequest:
    def __init__(self, name, raw_args=None, accepted_argc=(0,)):
        self.name = name
        self.raw_args = raw_args
        if len(raw_args) not in accepted_argc:
            raise ParseRequestError(f"wrong argument number: {len(raw_args)}")

    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        raise NotImplementedError

    def to_local_path(self, session: YAFTPSession, d: str = ".") -> str:
        def is_subpath(root, sub):
            root = os.path.abspath(root)
            sub = os.path.abspath(sub)
            return sub.startswith(root)
            
        path = os.path.join(session.root_dir, session.work_dir, d)
        if is_subpath(session.root_dir, path):
            return os.path.normpath(path)
        else:
            raise PathOverRootError(path)

    def to_virtual_path(self, session: YAFTPSession, d: str = ".") -> str:
        root = os.path.abspath(session.root_dir)
        local_path = os.path.abspath(self.to_local_path(session, d))  # have checked - is subpath of root path
        def remove_prefix(string, prefix):
            if string.startswith(prefix):
                return string[len(prefix):]
        removed = remove_prefix(local_path, root)
        if removed == "":   # FIXIT: a corner case. Refactor the path management part to clarify this
            return "/"
        else:
            return os.path.normpath(removed)

    def check_login_and_log(self, session: YAFTPSession):
        if not session.login:
            logging.info(f"try `{self}` without login")
            return False
        else:
            logging.info(f"execute `{self}` on {self.to_local_path(session, session.work_dir)}")
            return True

    def __str__(self):
        l = [self.name]
        l.extend(self.raw_args)
        return " ".join(l)

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
        if not self.check_login_and_log(session):
            return NotLoggedIn()
        try:
            path = self.to_local_path(session, self.dir)
        except PathOverRootError:
            return FileUnAvailable(self.dir)
        _, dirs, filenames = next(os.walk(path))
        dirs = list(map(lambda x: x + "/", dirs))
        return DirectoryStatus(dir_status="\n".join(dirs + filenames))

class YAFTPPwd(YAFTPRequest):
    def __init__(self, raw_args=None):
        super().__init__("PWD", raw_args, accepted_argc=(0,))

    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        if not self.check_login_and_log(session):
            return NotLoggedIn()
        path = self.to_virtual_path(session)
        return DirectoryStatus(dir_status=path)

class YAFTPCd(YAFTPRequest):
    """Only support relative path"""
    def __init__(self, raw_args=None):
        super().__init__("CD", raw_args, accepted_argc=(0, 1))
        self.relative_path = "."
        if len(raw_args) == 1:
            self.relative_path = raw_args[0]

    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        if not self.check_login_and_log(session):
            return NotLoggedIn()
        new_path = os.path.normpath(os.path.join(session.work_dir, self.relative_path))
        session.work_dir = new_path
        try:
            return DirectoryStatus(self.to_virtual_path(session))
        except PathOverRootError:
            return FileUnAvailable(self.relative_path)

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
    "CD": YAFTPCd,
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
