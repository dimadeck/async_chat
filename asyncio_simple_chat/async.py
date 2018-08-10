import asyncio
from asyncio_simple_chat.data_parser import DataParser
from asyncio_simple_chat.connected import Connected


class AsyncioChat:
    def __init__(self):
        self.connected = Connected()

    async def handle_client(self, reader, writer):
        while True:
            request = (await reader.read(1024))
            parse_list = DataParser(request)

            print(parse_list.data_list)  # DEBUG CODE

            self.connected.add_connection(writer)
            if parse_list.status == 0:
                self.run_command(parse_list, writer)
            else:
                self.send_message(writer, parse_list.STATUS_DICT[parse_list.status])

    def run_command(self, dictionary, connection):
        cmd = dictionary.cmd
        params = dictionary.parameter
        body = dictionary.body

        # DEBUG CODE START
        print(cmd)
        print(params)
        print(body)
        # DEBUG CODE END

        if cmd == 'login':
            self.connected.register_user(connection, params)
        elif cmd == 'msg':
            pass
        elif cmd == 'msgall':
            pass
            # for user in self.users.keys():
            #     user.write(bytes('Вам новое сообщение','utf-8'))
        elif cmd == 'logout':
            pass
        elif cmd == 'debug':
            pass
        elif cmd == 'whoami':
            pass
        elif cmd == 'userlist':
            pass

    def send_message(self, connection, message):
        connection.write(bytes(f'{message}\n', 'utf-8'))


def main():
    server = AsyncioChat()
    port = 10000
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(server.handle_client, '127.0.0.1', port))
    print(f'Server started on {port} port.')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()