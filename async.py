import asyncio


class AsyncioChat:
    def __init__(self):
        self.users = {}

    async def handle_client(self, reader, writer):
        while True:
            request = (await reader.read(255))
            request = request.decode('utf8').strip('\r\n')
            wordlist = request.split(' ')
            # print(wordlist)
            if wordlist[0] == 'login':
                print("dfsf")


if __name__ == '__main__':
    server = AsyncioChat()
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(server.handle_client, '127.0.0.1', 10000))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
