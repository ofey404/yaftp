from . import helpers
from socket import socket, AF_INET, SOCK_STREAM

class YAFTP:
    def __init__(self, address: (str, int) = ("127.0.0.1", 2121), user: str = '', passwd: str = ''):
        self.host = address[0]
        self.port = address[1]
        self.user = user
        self.passwd = passwd
        self.command_socket = socket(AF_INET, SOCK_STREAM)
        self.file_socket = None

    def __enter__(self):
        """For `with`, make this class a context manager type"""
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.quit()

    def login(self):
        self.command_socket.connect((self.host, self.port))

    def cwd(self, directory: str = "/"):
        pass

    def dir(self, directory: str = "/") -> str:
        self.command_socket.sendall(b'Hello world')
        data = self.command_socket.recv(1024)
        return "received: {}".format(data)

    def delete(self, filename: str):
        pass

    def quit(self):
        pass

