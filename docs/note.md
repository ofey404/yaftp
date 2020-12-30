# Develop Note

## background search
What interface does ftp provide?
- client:
    - open
    - get
    - send
    - dir
    - close/exit/bye

(refer to python's [ftplib](https://docs.python.org/3/library/ftplib.html) package)

How the messages are designed?

2 ports or 1 port?

out-of-band implementation is easier.

FTP has:
- simple command-response
- out-of-band two port structure
    - control link
    - file link(renew every file transfer)
- keep state during whole session

https://stackoverflow.com/questions/5953833/how-does-ftp-server-handle-multiple-connects-from-the-same-port

client: randomly choose a port for data and control connection.

Do I need to interact with GIL?
- GIL involves CPU-intensive programs. Network IO is not one of them.