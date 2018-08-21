import asyncio

from kernel.chat_kernel import ChatKernel
from kernel.chat_pack_message import PackMessage


class AsyncioChat(ChatKernel):
    def __init__(self, connections):
        super(AsyncioChat, self).__init__(connections=connections, method_send_message=self.send_message,
                                          method_close_connection=self.close_connection)
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


VERSION = 'AsyncIO_Chat'


def main(port=10000, connections=None):
    server = AsyncioChat(connections=connections)
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(server.handle_client, '127.0.0.1', port))
    print(PackMessage.server_message('start', version=VERSION, port=port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
