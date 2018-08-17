import asyncio

from base_server.tcp_server.tcp_kernel import TCPKernel


class AsyncioChat(TCPKernel):
    def __init__(self, connections):
        super(AsyncioChat, self).__init__(connections=connections)
        self.init_connection_list(connections)
    async def handle_client(self, reader, writer):
        while True:
            request = (await reader.read(1024))
            addr = writer.get_extra_info('peername')
            if self.engine(request, writer, addr) == -1:
                break

    @staticmethod
    def send_message(connection, message):
        connection.write(bytes(f'{message}\n', 'utf-8'))

    @staticmethod
    def close_connection(connection):
        connection.close()


def main(port=10000, connections=None):
    server = AsyncioChat(connections=connections)
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(server.handle_client, '127.0.0.1', port))
    print(f'[SERVER INFO] - AsyncIO server started on {port} port.')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
