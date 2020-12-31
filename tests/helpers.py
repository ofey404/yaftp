CORRECT_COMMANDS = [
    "LOGIN OFEY",
    "LOGIN OFEY:404",
    "DIR",
    "DIR test_folder",
    "DIR /",
    "PWD",
    "GET hello.txt",
    "GET test_folder/hey.txt",
    "GET /hello.txt",
    "GET /test_folder/hey.txt",
    "SEND this.txt",
    "BYE"
]

PARSE_RESULT = [
    ["LOGIN", "OFEY"],
    ["LOGIN", "OFEY", "404"],
    ["DIR"],
    ["DIR", "test_folder"],
    ["DIR", "/"],
    ["PWD"],
    ["GET", "hello.txt"],
    ["GET", "test_folder/hey.txt"],
    ["GET", "/hello.txt"],
    ["GET", "/test_folder/hey.txt"],
    ["SEND", "this.txt"],
    ["BYE"]
]