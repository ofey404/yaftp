import socket
import sys
s = socket.socket()
s.bind(("localhost",9999))
s.listen(10) # Acepta hasta 10 conexiones entrantes.
sc, address = s.accept()

print(address)
f = open("tmp",'wb') # Open in binary
# Recibimos y escribimos en el fichero
l = sc.recv(1024)
while (l):
    f.write(l)
    l = sc.recv(1024)
f.close()

sc.close()
s.close()
