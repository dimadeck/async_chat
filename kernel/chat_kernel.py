from kernel.chat_pack_message import PackMessage
from kernel.chat_protocol import ChatProtocol
from kernel.connected import Connected
from kernel.data_parser import DataParser


class ChatKernel:
    def __init__(self, setup):
        self.connections = self.init_connection_list(setup['connections'])
        self.parse_strip = setup['parse_strip']
        if setup['method_send_message'] is not None:
            self.send_message = setup['method_send_message']
        if setup['method_close_connection'] is not None:
            self.close_connection = setup['method_close_connection']
        self.version = setup['version']
        self.pack_message = PackMessage(version=self.version)
        print(self.pack_message.server_message('start', port=setup['port']))

    @staticmethod
    def init_connection_list(connections):
        return connections if connections is not None else Connected()

    def send_all(self, message):
        for user in self.get_users():
            self.send_message(user, message)

    def login(self, connection, username):
        return self.connections.register_user(connection, username)

    def logout(self, connection):
        self.close_connection(connection)
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

    def engine(self, request, writer, addr):
        if len(request) > 0:
            if self.add_connection(writer) == 0:
                print(self.pack_message.server_message('new', addr=addr))
            req_dict = DataParser(request, strip=self.parse_strip)
            if req_dict.status == 0:
                return self.run_command(req_dict, writer)
            else:
                message = self.pack_message.system_error('bad_request', message=req_dict.STATUS_DICT[req_dict.status])
                self.send_message(writer, message)
        elif not request:
            self.logout_engine(writer)
            return -1
        return 0

    def run_command(self, req_dict, connection):
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
                       'whoami': (self.whoami_engine, {'connection': connection, 'clear_data': req_dict.clear_data}),
                       'userlist': (self.userlist_engine, {'connection': connection, 'clear_data': req_dict.clear_data})
                       }
        else:
            methods = {'login': (self.login_engine, {'connection': connection, 'username': param}),
                       'empty': (self.error_first_login, {'connection': connection})}
        protocol = ChatProtocol(**methods)
        return protocol.engine(cmd)

    def logout_engine(self, connection):
        username = self.get_name_by_connection(connection)
        if username != 0:
            self.logout(connection)
            message = self.pack_message.system_message('logout', username=username)
            self.send_all(message)
            print(self.pack_message.server_message('logout', username=username))
            return -1

    def login_engine(self, connection, username):
        if self.login(connection, username) == 0:
            print(self.pack_message.server_message('login', username=username))
            message = self.pack_message.system_message('login', username=username)
            self.send_all(message)
        else:
            message = self.pack_message.system_error('user_exist')
            self.send_message(connection, message)

    def error_alredy_login(self, connection):
        message = self.pack_message.system_error('already_login')
        self.send_message(connection, message)

    def error_first_login(self, connection):
        message = self.pack_message.system_error('first_login')
        self.send_message(connection, message)

    def send_message_engine(self, connection, username, message):
        sender = self.get_name_by_connection(connection)
        user = self.get_connection_by_name(username)
        if user is not None:
            message = self.pack_message.chat_message(username=sender, message=message, private=True)
            self.send_message(user, message)
            self.send_message(connection, message)
        else:
            message = self.pack_message.system_error('not_found', username=username)
            self.send_message(connection, message)

    def send_all_engine(self, connection, message):
        sender = self.get_name_by_connection(connection)
        message = self.pack_message.chat_message(username=sender, message=message)
        self.send_all(message)

    def debug_engine(self):
        connections = self.get_connections()
        userlist = self.get_users()

        print(self.pack_message.message(connections))
        print(self.pack_message.message(userlist))

    def whoami_engine(self, connection, clear_data):
        username = self.get_name_by_connection(connection)
        message = self.pack_message.system_info(username, clear_data)
        self.send_message(connection, message)

    def userlist_engine(self, connection, clear_data):
        userlist = ', '.join(self.get_username_list())
        message = self.pack_message.system_info(userlist, clear_data)
        if 'WS' in self.version and clear_data:
            message = message.split(sep=', ')
        self.send_message(connection, message)
