import socket

host = '127.0.0.1'
port = 2121

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as t:
        s.connect((host, port))
        t.listen(port+1)
        while True:
            i = input("> ")
            s.sendall(bytes(i, 'utf-8'))
            data = s.recv(1024)
            print(data.decode())