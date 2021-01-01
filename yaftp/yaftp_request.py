from .exception import ParseRequestError, PathOverRootError
from .yaftp_session import YAFTPSession
from .yaftp_response import YAFTPResponse, InvalidUserNameOrPassword, UserLoggedIn, NotLoggedIn, DirectoryStatus, FileUnAvailable, UserLoggedOut, FileStatus
import logging
import os
from time import sleep
import threading
import socket
from .virtual_path import VirtualPath, local_to_virtual_abs 

class YAFTPRequest:
    def __init__(self, name, raw_args=(), accepted_argc=(0,)):
        self.name = name
        self.raw_args = raw_args
        if len(raw_args) not in accepted_argc:
            raise ParseRequestError(f"wrong argument number: {len(raw_args)}")

    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        raise NotImplementedError

    def check_login_and_log(self, session: YAFTPSession):
        if not session.login:
            logging.info(f"try `{self}` without login")
            return False
        else:
            logging.info(f"execute `{self}`, work dir: {session.work_dir}, root dir: {session.root_dir}")
            return True

    def __str__(self):
        l = [self.name]
        l.extend(self.raw_args)
        return " ".join(l)

class YAFTPLogin(YAFTPRequest):
    def __init__(self, raw_args=()):
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
    def __init__(self, raw_args=()):
        super().__init__("DIR", raw_args, accepted_argc=(0, 1))
        self.dir = VirtualPath('.')
        if len(raw_args) != 0:
            self.dir = VirtualPath(raw_args[0])
    
    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        if not self.check_login_and_log(session):
            return NotLoggedIn()
        try:
            path = self.dir.to_local_path(session.work_dir, session.root_dir)
        except PathOverRootError:
            return FileUnAvailable(self.dir)
        logging.debug(f"try to dir in {path}")
        _, dirs, filenames = next(os.walk(path))
        dirs = list(map(lambda x: x + "/", dirs))
        return DirectoryStatus(dir_status="\n".join(dirs + filenames))

class YAFTPPwd(YAFTPRequest):
    def __init__(self, raw_args=()):
        super().__init__("PWD", raw_args, accepted_argc=(0,))

    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        if not self.check_login_and_log(session):
            return NotLoggedIn()
        path = local_to_virtual_abs(session.work_dir, session.root_dir)
        return DirectoryStatus(dir_status=path)

class YAFTPCd(YAFTPRequest):
    def __init__(self, raw_args=()):
        super().__init__("CD", raw_args, accepted_argc=(0, 1))
        self.virtpath = VirtualPath("/")
        if len(raw_args) == 1:
            self.virtpath = VirtualPath(raw_args[0])

    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        if not self.check_login_and_log(session):
            return NotLoggedIn()

        new_path = self.virtpath.to_local_path(session.work_dir, session.root_dir)
        session.work_dir = new_path
        logging.debug(f"try to switch to {new_path}")
        try:
            return DirectoryStatus(str(self.virtpath))
        except PathOverRootError:
            return FileUnAvailable(str(self.virtpath))

class YAFTPGet(YAFTPRequest):
    """Active Mode Only"""
    def __init__(self, raw_args=()):
        super().__init__("GET", raw_args, accepted_argc=(2,))
        self.filepath = VirtualPath(raw_args[0])
        self.client_hostname = None
        self.client_dataport = None
        try:
            self.client_dataport = int(raw_args[1])
        except ValueError:
            raise ParseRequestError(f"can't parse client data port: {raw_args[1]}")

    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        if not self.check_login_and_log(session):
            return NotLoggedIn()
        self.client_hostname = session.client_address[0]

        try:
            path = self.filepath.to_local_path(session.work_dir, session.root_dir)
        except PathOverRootError:
            return FileUnAvailable(str(self.filepath))

        if not os.path.isfile(path):
            return FileUnAvailable(str(self.filepath))

        def send_file_to_client():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                try:
                    client_data_addr = (self.client_hostname, self.client_dataport)
                    s.connect(client_data_addr)
                except socket.timeout:
                    return
                with open(path, "rb") as f:
                    l = f.read(1024)
                    while l:
                        s.send(l)
                        l = f.read(1024)
        
        threading.Thread(
            target=send_file_to_client
        ).start()

        return FileStatus(f"try sending file {str(self.filepath)} to {self.client_hostname}:{self.client_dataport}")

class YAFTPSend(YAFTPRequest):
    def __init__(self, raw_args=()):
        super().__init__("SEND", raw_args, accepted_argc=(2,))
        self.filepath = VirtualPath(raw_args[0])
        self.client_hostname = None
        self.client_dataport = None
        try:
            self.client_dataport = int(raw_args[1])
        except ValueError:
            raise ParseRequestError(f"can't parse client data port: {raw_args[1]}")

    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        if not self.check_login_and_log(session):
            return NotLoggedIn()
        self.client_hostname = session.client_address[0]

        try:
            path = self.filepath.to_local_path(session.work_dir, session.root_dir)
        except PathOverRootError:
            return FileUnAvailable(self.filepath)

        def receive_file_from_client():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                try:
                    client_data_addr = (self.client_hostname, self.client_dataport)
                    s.connect(client_data_addr)
                except socket.timeout:
                    return
                with open(path, "wb") as f:
                    l = s.recv(1024)
                    while l:
                        f.write(l)
                        l = s.recv(1024)

        threading.Thread(
            target=receive_file_from_client
        ).start()

        return FileStatus(f"try receiving file {str(self.filepath)} from {self.client_hostname}:{self.client_dataport}")

class YAFTPDelete(YAFTPRequest):
    def __init__(self, raw_args=()):
        super().__init__("DELETE", raw_args=raw_args, accepted_argc=(1,))
        self.filepath = VirtualPath(raw_args[0])

    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        if not self.check_login_and_log(session):
            return NotLoggedIn()

        try:
            path = self.filepath.to_local_path(session.work_dir, session.root_dir)
        except PathOverRootError:
            return FileUnAvailable(self.filepath)

        if not os.path.isfile(path):
            return FileUnAvailable(self.filepath)

        os.remove(path)
        return FileStatus(f"deleted file {str(self.filepath)}")

class YAFTPBye(YAFTPRequest):
    def __init__(self, raw_args=()):
        super().__init__("BYE", raw_args, accepted_argc=(0,))

    def execute(self, session: YAFTPSession) -> YAFTPResponse:
        if not self.check_login_and_log(session):
            return NotLoggedIn()
        session.ended = True
        return UserLoggedOut()

REQUESTS = {
    "LOGIN": YAFTPLogin,
    "DIR": YAFTPDir,
    "PWD": YAFTPPwd,
    "CD": YAFTPCd,
    "GET": YAFTPGet,
    "SEND": YAFTPSend,
    "DELETE": YAFTPDelete,
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
