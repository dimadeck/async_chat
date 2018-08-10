import asyncio
from asyncio_simple_chat.data_parser import DataParser
from asyncio_simple_chat.connected import Connected


class AsyncioChat:
    def __init__(self):
        self.connected = Connected()

    async def handle_client(self, reader, writer):
        while True:
            request = (await reader.read(1024))
            if len(request) > 1:
                parse_list = DataParser(request)

                print(f'Request: {parse_list.data_list}')  # DEBUG LINE

                if self.connected.get_name(writer) == 0:
                    self.connected.add_connection(writer)

                if parse_list.status == 0:
                    if self.run_command(parse_list, writer) == -1:
                        break
                else:
                    self.send_message(writer, parse_list.STATUS_DICT[parse_list.status])
            if not request:
                self.logout(writer)
                break

    def run_command(self, req_dict, connection):
        cmd = req_dict.cmd
        param = req_dict.parameter
        body = req_dict.body
        print(f'Command: {cmd}\nParameter: {param}\nBody: {body}')  # DEBUG LINE

        if self.connected.is_register(connection):
            if cmd == 'msg' or cmd == 'msgall':
                self.send_engine(connection, cmd, param, body)
            elif cmd == 'logout':
                self.logout(connection)
                return -1
            elif cmd == 'debug':
                print(self.connected.connections)
                print(self.connected.users)
            elif cmd == 'whoami':
                self.send_message(connection, self.connected.get_name(connection))
            elif cmd == 'userlist':
                self.send_message(connection, self.connected.get_user_list())
            elif cmd == 'login':
                self.send_message(connection, 'Already login!')
        else:
            if cmd == 'login':
                self.login(connection, param)
            else:
                self.send_message(connection, 'First login!')
        return 0

    def send_engine(self, connection, cmd, param, body):
        sender = self.connected.get_name(connection)
        message = ' '.join(body)
        if cmd == 'msg':
            user = self.connected.get_connection(param)
            if user is not None:
                self.send_message(user, f'[{sender}*]: {message}')
                self.send_message(connection, f'[{sender}*]: {message}')
            else:
                self.send_message(connection, f'[{user}]: not found!')
        elif cmd == 'msgall':
            self.send_all(f'[{sender}]: {message}')

    @staticmethod
    def send_message(connection, message):
        connection.write(bytes(f'{message}\n', 'utf-8'))

    def send_all(self, message):
        for user in self.connected.users.keys():
            self.send_message(user, message)

    def login(self, connection, username):
        self.connected.register_user(connection, username)
        self.send_all(f'[System Message]: [{username}] login to chat.')

    def logout(self, connection):
        username = self.connected.get_name(connection)
        connection.close()
        self.connected.drop_connection(connection)
        self.send_all(f'[System Message]: [{username}] logout from chat.')


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
