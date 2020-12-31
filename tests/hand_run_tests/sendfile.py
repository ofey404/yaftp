import socket
import sys

s = socket.socket()
s.bind(("127.0.0.1", 11111))
s.listen()
sc, address = s.accept()

print(address)

f = open ("LICENSE", "rb")
l = f.read(1024)
while (l):
    sc.send(l)
    l = f.read(1024)

sc.close()
s.close()
