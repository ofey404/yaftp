import socket
import sys
s = socket.socket()
s.connect(("localhost",9999))

f = open("tmp",'wb') # Open in binary
# Recibimos y escribimos en el fichero
l = s.recv(1024)
while (l):
    f.write(l)
    l = s.recv(1024)
f.close()

s.close()
