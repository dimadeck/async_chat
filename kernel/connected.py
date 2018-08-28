import asyncio
import sys
from time import sleep


class Connected:
    connections = []
    users = {}

    @staticmethod
    def clear_all():
        Connected.connections = []
        Connected.users = {}

    @staticmethod
    def add_connection(connection):
        if not Connected.is_exist_connection(connection):
            Connected.connections.append(connection)
            return 0
        else:
            return -1

    @staticmethod
    def is_exist_connection(connection):
        return connection in Connected.connections

    @staticmethod
    def is_valid_name(username):
        if username in Connected.users.values():
            return -1
        else:
            return 0

    @staticmethod
    def register_user(connection, username):
        if Connected.is_valid_name(username) == 0:
            Connected.users[connection] = username
            return 0
        return -1

    @staticmethod
    def is_register(connection):
        return connection in Connected.users

    @staticmethod
    def get_connection(username):
        for connection in Connected.connections:
            if username == Connected.users[connection]:
                return connection
        return None

    @staticmethod
    def get_name(connection):
        try:
            return Connected.users[connection]
        except KeyError:
            return 0

    @staticmethod
    def drop_connection(connection):
        if Connected.is_register(connection):
            Connected.users.pop(connection)
        if connection in Connected.connections:
            Connected.connections.remove(connection)

    @staticmethod
    def get_username_list():
        user_list = []
        for username in Connected.users.values():
            user_list.append(username)
        return user_list

    @staticmethod
    def get_connections():
        return Connected.connections

    @staticmethod
    def get_users():
        return Connected.users


class ConnectedServer:
    def __init__(self):
        self.connections = Connected

    async def handle_client(self, reader, writer):
        while True:
            request = (await reader.read(1024))
            if len(request) > 0:
                req_dict = self.parse_request(request)
                print(req_dict)
                answer = self.engine(req_dict)
                writer.write(bytes(f'{answer}', 'utf-8'))

    def parse_request(self, request):
        req_words = request.decode('utf-8').strip('\r\n').split(' ')
        return {'cmd': req_words[0], 'args': req_words[1:]}

    def engine(self, req_dict):
        cmd = req_dict['cmd']
        args = req_dict['args']
        answer_set = {
            'register_user': self.connections.register_user,
            'drop_connection': self.connections.drop_connection,
            'add_connection': self.connections.add_connection,
            'is_register': self.connections.is_register,
            'get_connections': self.connections.get_connections,
            'clear_all': self.connections.clear_all,
            'get_users': self.connections.get_users,
            'get_name': self.connections.get_name,
            'get_connection': self.connections.get_connection,
            'get_username_list': self.connections.get_username_list,
        }
        try:
            return answer_set[cmd](*args)
        except:
            return -100
        # register_user(connection, username)
        # drop_connection(connection)
        # add_connection(connection)
        # is_register(connection)
        # get_connections()
        # clear_all()
        # get_users()
        # get_name(connection)
        # get_connection(username)
        # get_username_list()


class ConnectedClient:
    def __init__(self):
        self.conn_read = None
        self.conn_write = None
        self.loop = asyncio.get_event_loop()
        self.engine()

    async def send_request(self, request):
        await self.conn_write.write(bytes(request, encoding='utf-8'))
        data = await self.conn_read.read(100)
        print(data.decode())

    def register_user(self, connection, username):
        return self.send_request(f'register_user {connection} {username}')

    def drop_connection(self, connection):
        self.send_request(f'drop_connection {connection}')

    def add_connection(self, connection):
        return self.send_request(f'add_connection {connection}')

    def is_register(self, connection):
        return self.send_request(f'is_register {connection}')

    def get_connections(self):
        return self.send_request(f'get_connections')

    def clear_all(self):
        self.send_request(f'clear_all')

    def get_users(self):
        return self.send_request(f'get_users')

    def get_name(self, connection):
        return self.send_request(f'get_name {connection}')

    def get_connection(self, username):
        return self.send_request(f'get_connection {username}')

    def get_username_list(self):
        return self.send_request(f'get_username_list')

    async def handle_client(self):
        self.conn_read, self.conn_write = await asyncio.open_connection('127.0.0.1', 10000, loop=self.loop)

    def engine(self):
        self.loop.run_until_complete(self.handle_client())

    def test(self):
        self.add_connection('1')
        self.register_user('1', '2')
        self.get_username_list()

    def close(self):
        print('close')
        self.loop.close()


def main(port=10000):
    server = ConnectedServer()
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(server.handle_client, '127.0.0.1', port))
    print(f'Connection server start on port{port}')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()


def main_client():
    client = ConnectedClient()
    sleep(4)
    client.close()


if __name__ == '__main__':
    if sys.argv[1] == 'client':
        main_client()
    else:
        main()
