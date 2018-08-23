from kernel.chat_pack_message import PackMessage
from kernel.chat_protocol import ChatProtocol
from kernel.connected import Connected
from kernel.data_parser import DataParser


class ChatKernel:
    def __init__(self, connections=None, parse_strip='\r\n', method_send_message=None, method_close_connection=None,
                 version=None, port=None):
        self.connections = self.init_connection_list(connections)
        self.parse_strip = parse_strip
        if method_send_message is not None:
            self.send_message = method_send_message
        if method_close_connection is not None:
            self.close_connection = method_close_connection
        self.init_connection_list(connections)
        self.version = version
        self.pack_message = PackMessage(version=version)
        print(self.pack_message.server_message('start', port=port))

    @staticmethod
    def init_connection_list(connections):
        return connections if connections is not None else Connected()

    @staticmethod
    def send_message(connection, message):
        raise NotImplementedError

    @staticmethod
    def close_connection(connection):
        raise NotImplementedError

    async def send_all(self, message):
        for user in self.get_users():
            await self.send_message(user, message)

    def login(self, connection, username):
        return self.connections.register_user(connection, username)

    async def logout(self, connection):
        await self.close_connection(connection)
        self.connections.drop_connection(connection)

    def add_connection(self, connection):
        return self.connections.add_connection(connection)

    def is_register(self, connection):
        return self.connections.is_register(connection)

    def get_connections(self):
        return self.connections.connections

    def clear_connections(self):
        self.connections.clear_all()

    def get_users(self):
        return self.connections.users

    def get_name_by_connection(self, connection):
        return self.connections.get_name(connection)

    def get_connection_by_name(self, username):
        return self.connections.get_connection(username)

    def get_username_list(self):
        return self.connections.get_username_list()

    async def engine(self, request, writer, addr):
        if len(request) > 0:
            if self.add_connection(writer) == 0:
                print(self.pack_message.server_message('new', addr=addr))
            req_dict = DataParser(request, strip=self.parse_strip)
            if req_dict.status == 0:
                return await self.run_command(req_dict, writer)
            else:
                message = self.pack_message.system_error('bad_request', message=req_dict.STATUS_DICT[req_dict.status])
                await self.send_message(writer, message)
        elif not request:
            await self.logout_engine(writer)
            return -1
        return 0

    async def run_command(self, req_dict, connection):
        cmd = req_dict.cmd
        param = req_dict.parameter
        body = req_dict.body
        message = ' '.join(req_dict.body) if body is not None else None

        if self.is_register(connection):
            methods = {'login': (self.error_alredy_login, {'connection': connection}),
                       'logout': (self.logout_engine, {'connection': connection}),
                       'msg': (
                           self.send_message_engine, {'connection': connection, 'username': param, 'message': message}),
                       'msgall': (self.send_all_engine, {'connection': connection, 'message': message}),
                       'debug': (self.debug_engine, {}),
                       'whoami': (self.whoami_engine, {'connection': connection}),
                       'userlist': (self.userlist_engine, {'connection': connection})
                       }
        else:
            methods = {'login': (self.login_engine, {'connection': connection, 'username': param}),
                       'empty': (self.error_first_login, {'connection': connection})}
        protocol = ChatProtocol(**methods)
        return await protocol.engine(cmd)

    async def logout_engine(self, connection):
        username = self.get_name_by_connection(connection)
        if username != 0:
            await self.logout(connection)
            message = self.pack_message.system_message('logout', username=username)
            await self.send_all(message)
            print(self.pack_message.server_message('logout', username=username))
            return -1

    async def login_engine(self, connection, username):
        if self.login(connection, username) == 0:
            print(self.pack_message.server_message('login', username=username))
            message = self.pack_message.system_message('login', username=username)
            await self.send_all(message)
        else:
            message = self.pack_message.system_error('user_exist')
            await self.send_message(connection, message)

    async def error_alredy_login(self, connection):
        message = self.pack_message.system_error('already_login')
        await self.send_message(connection, message)

    async def error_first_login(self, connection):
        message = self.pack_message.system_error('first_login')
        await self.send_message(connection, message)

    async def send_message_engine(self, connection, username, message):
        sender = self.get_name_by_connection(connection)
        user = self.get_connection_by_name(username)
        if user is not None:
            message = self.pack_message.chat_message(username=sender, message=message, private=True)
            await self.send_message(user, message)
            await self.send_message(connection, message)
        else:
            message = self.pack_message.system_error('not_found', username=username)
            await self.send_message(connection, message)

    async def send_all_engine(self, connection, message):
        sender = self.get_name_by_connection(connection)
        message = self.pack_message.chat_message(username=sender, message=message)
        await self.send_all(message)

    def debug_engine(self):
        connections = self.get_connections()
        userlist = self.get_users()

        print(self.pack_message.message(connections))
        print(self.pack_message.message(userlist))

    async def whoami_engine(self, connection):
        username = self.get_name_by_connection(connection)
        message = self.pack_message.system_info(username)
        await self.send_message(connection, message)

    async def userlist_engine(self, connection):
        userlist = f"[{', '.join(self.get_username_list())}]"
        message = self.pack_message.system_info(userlist)
        await self.send_message(connection, message)
