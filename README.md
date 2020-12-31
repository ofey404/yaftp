# yaftp: Yet another file transfer protocol
A simple ftp-like file transfer protocol package.

Weiwen Chen's fifth project of Computer Network course in FDU.

## Usage

### Set up a server
```python
import yaftp

yaftp.YAFTPServer(
    address=("127.0.0.1", 2121),
    local_dir="tests/data",
    auth={
        "USER": "PASSWORD",
        "OFEY": "404",
        "ANONYMOUS": ""   # Blank means login without password
    }
).serve()
```

### Interact with a server
```python
import yaftp

c = yaftp.YAFTP(
    address=("127.0.0.1", 2121),
    user="USER",
    passwd="PASSWORD"
)

c.login()
# Out[2]: 230

c.dir()
# Out[3]: ['test_folder/', 'hello.txt', 'hey.txt']

c.get(name="hello.txt", savepath="saved_file")
# Out[4]: 213

%cat saved_file
# hello from the other side!

c.send(filepath="saved_file", name="hey.txt")
# Out[6]: 213

c.dir()
# Out[7]: ['test_folder/', 'hello.txt', 'hey.txt']

c.cd(path="test_folder")
# Out[8]: 212

c.dir()
# Out[9]: ['hey.txt']

c.quit()
# Out[10]: 231
```

## Reference
- https://en.wikipedia.org/wiki/List_of_FTP_server_return_codes

API Design refer to:
- https://docs.python.org/3/library/ftplib.html
- https://pyftpdlib.readthedocs.io/en/latest/index.html