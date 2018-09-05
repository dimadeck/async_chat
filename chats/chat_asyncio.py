import asyncio

from chats import AsServer
from kernel.fork_chat_kernel import ChatKernel
from kernel.fork_sender import Sender


class AsyncioChat:
    def __init__(self, chat):
        self.chat = chat

    async def handle_client(self, reader, writer):
        while True:
            try:
                request = (await reader.read(1024))
                addr = writer.get_extra_info('peername')
                request = request.decode('utf-8').strip('\r\n')
                if await self.chat.engine(request, writer, addr) == -1:
                    break
            except:
                await self.chat.logout_engine(writer)
                break


def main(port=8000):
    chat = ChatKernel(AsServer, port, sender=Sender())
    server = AsyncioChat(chat)
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(server.handle_client, '127.0.0.1', port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
