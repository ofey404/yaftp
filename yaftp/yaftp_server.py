import threading
from socket import socket, AF_INET, SOCK_STREAM

def handle_control_connection(client_socket, addr):
    print('connected by: {}'.format(addr))
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        client_socket.sendall(data)

class YAFTPServer:
    def __init__(self, address: (str, int) = ("127.0.0.1", 2121), local_dir='.'):
        self.host = address[0]
        self.port = address[1]
        self.local_dir = local_dir

    def serve(self):
        with socket(AF_INET, SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                c, addr = s.accept()
                t = threading.Thread(target=handle_control_connection, args=(c, addr))
                t.start()
