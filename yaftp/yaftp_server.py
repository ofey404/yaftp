import logging
import socket
import asyncio

class YAFTPServer:
    def __init__(self, address: (str, int) = ("127.0.0.1", 2121), local_dir='.'):
        self.host = address[0]
        self.port = address[1]
        self.local_dir = local_dir
        logging.basicConfig(format='%(process)d - [%(levelname)s] - %(asctime)s - %(message)s', datefmt='%y-%m-%d %H:%M:%S', level=logging.INFO)
        self.loop = asyncio.get_event_loop()
        self.server = None

    def serve(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(8)
        self.server.setblocking(False)
        self.loop.run_until_complete(self.run_server())

    async def run_server(self):
        if self.server == None:
            return
        while True:
            client, address = await self.loop.sock_accept(self.server)
            logging.info(f'connected by: {address[0]}:{address[1]}')
            self.loop.create_task(self.handler(client, address))

    async def handler(self, client_socket, address):
        while True:
            data = (await self.loop.sock_recv(client_socket, 1024)).decode('utf8')
            if not data:
                break
            await self.loop.sock_sendall(client_socket, data.encode('utf8'))

    def close_all(self):
        self.server.close()
