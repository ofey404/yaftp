from . import helpers
from socket import socket, AF_INET, SOCK_STREAM
from .yaftp_request import YAFTPRequest, YAFTPLogin, YAFTPPwd, YAFTPDir, YAFTPCd, YAFTPGet, YAFTPSend, YAFTPBye
from .yaftp_response import YAFTPResponse, YAFTPResponseParser
import threading

class YAFTP:
    def __init__(self, address: (str, int) = ("127.0.0.1", 2121), user: str = 'OFEY', passwd: str = '404'):
        self.host = address[0]
        self.port = address[1]
        self.user = user
        self.passwd = passwd
        self.command_socket = None
        self.file_socket = None

    def __enter__(self):
        """For `with`, make this class a context manager type"""
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.quit()

    def login(self) -> int:
        self.command_socket = socket(AF_INET, SOCK_STREAM)
        self.command_socket.connect((self.host, self.port))
        if self.passwd == None:
            request = YAFTPLogin([f"{self.user}"])
        else:
            request = YAFTPLogin([f"{self.user}:{self.passwd}"])
        return self.get_code(self.send_request(request))

    def pwd(self) -> str:
        return self.send_request(YAFTPPwd()).split("\n", 1)[1]

    def cd(self, path=".") -> int:
        return self.get_code(self.send_request(YAFTPCd([path])))

    def dir(self, directory: str = ".") -> [str]:
        return self.send_request(YAFTPDir([directory])).split("\n")[1:]

    def send(self, filepath, name) -> int:
        file_socket = socket(AF_INET, SOCK_STREAM)
        file_socket.settimeout(10)
        file_socket.bind(("", 0))
        file_socket.listen()
        dataport = file_socket.getsockname()[1]
        def send_file():
            sc, _ = file_socket.accept()
            with open(filepath, "rb") as f:
                l = f.read(1024)
                while l:
                    sc.send(l)
                    l = f.read(1024)
            sc.close()
            file_socket.close()
        threading.Thread(target=send_file).start()
        response = self.send_request(YAFTPSend([name, str(dataport)]))
        return self.get_code(response)

    def get(self, name, savepath) -> int:
        file_socket = socket(AF_INET, SOCK_STREAM)
        file_socket.settimeout(10)
        file_socket.bind(("", 0))
        file_socket.listen()
        dataport = file_socket.getsockname()[1]

        def get_file():
            sc, _ = file_socket.accept()
            with open(savepath, "wb") as f:
                l = sc.recv(1024)
                while l:
                    f.write(l)
                    l = sc.recv(1024)
            sc.close()
            file_socket.close()

        threading.Thread(target=get_file).start()
        response = self.send_request(YAFTPGet([name, str(dataport)]))
        return self.get_code(response)

    def quit(self) -> int:
        response = self.send_request(YAFTPBye())
        self.command_socket.close()
        return self.get_code(response)

    def send_request(self, request: YAFTPRequest) -> str:
        self.command_socket.sendall(bytes(str(request), 'utf-8'))
        data = self.command_socket.recv(1024)
        return data.decode()

    def get_code(self, raw_response: str) -> int:
        return YAFTPResponseParser().from_string(raw_response).code
