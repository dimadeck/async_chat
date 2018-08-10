import asyncio
from base_server.base_server import ChatKernel


class AsyncioChat(ChatKernel):

    async def handle_client(self, reader, writer):
        while True:
            request = (await reader.read(1024))
            if self.engine(request, writer) == -1:
                break


def main():
    server = AsyncioChat()
    port = 10000
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(server.handle_client, '127.0.0.1', port))
    # if SERVER_INFO:
    print(f'[SERVER INFO] - Server started on {port} port.')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
