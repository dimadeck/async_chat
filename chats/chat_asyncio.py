import asyncio

from chats import VERSION_AS as VERSION, get_setup_dict
from kernel.fork_chat_kernel import ChatKernel


class AsyncioChat:
    def __init__(self, connections, port):
        setup_dict = get_setup_dict(connections, VERSION, port)
        self.chat = ChatKernel(setup_dict)

    async def handle_client(self, reader, writer):
        while True:
            request = (await reader.read(1024))
            addr = writer.get_extra_info('peername')
            if await self.chat.engine(request, writer, addr) == -1:
                break


def main(port=10000, connections=None):
    server = AsyncioChat(connections=connections, port=port)
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(server.handle_client, '127.0.0.1', port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
