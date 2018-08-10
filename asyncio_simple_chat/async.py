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

            print(f'Request: {parse_list.data_list}')  # DEBUG LINE

            self.connected.add_connection(writer)
            if parse_list.status == 0:
                self.run_command(parse_list, writer)
            else:
                self.send_message(writer, parse_list.STATUS_DICT[parse_list.status])

    def run_command(self, dictionary, connection):
        cmd = dictionary.cmd
        param = dictionary.parameter
        body = dictionary.body
        print(f'Command: {cmd}\nParameter: {param}\nBody: {body}')  # DEBUG LINE

        if cmd == 'login':
            self.connected.register_user(connection, param)
        elif cmd == 'msg' or cmd == 'msgall':
            sender = self.connected.get_name(connection)
            message = ' '.join(body)

            if cmd =='msg':
                user = self.connected.get_connection(param)
                if user is not None:
                    self.send_message(user, f'[{sender}*]: {message}')
                    self.send_message(connection, f'[{sender}*]: {message}')
                else:
                    self.send_message(connection, f'[{user}]: not found!')

            elif cmd =='msgall':
                for user in self.connected.users.keys():
                    self.send_message(user, f'[{sender}]: {message}')

        elif cmd == 'logout':
            pass
        elif cmd == 'debug':
            print(self.connected.connections)
            print(self.connected.users)
        elif cmd == 'whoami':
            self.send_message(connection, self.connected.get_name(connection))

        elif cmd == 'userlist':
            self.send_message(connection, self.connected.get_user_list())

    @staticmethod
    def send_message(connection, message):
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
