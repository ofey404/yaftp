import logging
import socket
import asyncio
from .yaftp_request import YAFTPRequestParser
from .yaftp_response import YAFTPResponse, InvalidCommandOrArguments
from .yaftp_session import YAFTPSession
from .exception import ParseRequestError

class YAFTPServer:
    def __init__(self, address: (str, int) = ("127.0.0.1", 2121), local_dir='.', auth={"OFEY": "404"}):
        self.host = address[0]
        self.port = address[1]
        self.local_dir = local_dir
        logging.basicConfig(format='%(process)d - [%(levelname)s] - %(asctime)s - %(message)s', datefmt='%y-%m-%d %H:%M:%S', level=logging.DEBUG)
        self.loop = asyncio.get_event_loop()
        self.server = None
        self.auth = auth

    def serve(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(8)
        self.server.setblocking(False)
        self.loop.run_until_complete(self.server_loop())

    async def server_loop(self):
        if self.server == None:
            return
        while True:
            client, address = await self.loop.sock_accept(self.server)
            logging.info(f'connected by: {address[0]}:{address[1]}')
            self.loop.create_task(self.handler(client, address))

    async def handler(self, client_socket, address):
        logging.debug(f'start handling, client: {client_socket}')
        session = YAFTPSession(
            root_dir=self.local_dir,
            authenticator=self.auth,
            client_address = address
            )
        # TODO: set a timeout.
        while not session.ended:
            request_string = (await self.loop.sock_recv(client_socket, 1024)).decode()
            if not request_string:
                logging.debug(f'no more requests')
                break
            try:
                request = YAFTPRequestParser().parse(request_string)
                response = request.execute(session)  # TODO: await this
            except ParseRequestError:
                response = InvalidCommandOrArguments()
            await self.loop.sock_sendall(client_socket, str(response).encode())
        logging.debug(f'end handling, client: {client_socket}')


    def close_all(self):
        self.server.close()
