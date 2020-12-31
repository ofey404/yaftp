# yaftp: Yet another file transfer protocol
Weiwen Chen's fifth project of Computer Network course in FDU.

A simple ftp-like file transfer protocol package.

## Usage

### Installation
```bash
git clone https://github.com/ofey404/yaftp.git
cd yaftp
pip install -e .
```

Then you can use `yaftp` package in python:

```bash
$ python
Python 3.9.1 (default, Dec  8 2020, 00:00:00) 
[GCC 10.2.1 20201125 (Red Hat 10.2.1-9)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import yaftp
>>> 
```

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

## Implementation detail
Super simple, just a toy, never care about performance. 

Use async event loop to handle control connection, while firing other threads to deal with data connection.

### Commands
- `LOGIN USER[:PASSWORD]`
- `DIR [RELATIVE_PATH]`
- `PWD`
- `CD [RELATIVE_PATH]`
- `GET FILENAME DATA_PORT`
    - DATA_PORT should be opened in localhost before command is executed.
- `SEND FILENAME DATA_PORT`
    - DATA_PORT: same as above.
- `BYE`

## Only support active mode
Implemented a ftp-like active mode, because it's easy, without much synchronizaion effort.

When sending or getting a file:
- Client open a local data port, listening.
- Client -- request --> Server
    - request specify the data port.
- Server -- connect --> Client:data_port
    - then send file.

## Reference
- https://en.wikipedia.org/wiki/List_of_FTP_server_return_codes

API Design refer to:
- https://docs.python.org/3/library/ftplib.html
- https://pyftpdlib.readthedocs.io/en/latest/index.html