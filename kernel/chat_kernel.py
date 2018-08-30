from kernel.chat_pack_message import PackMessage
from kernel.chat_protocol import ChatProtocol
from kernel.connected import Connected
from kernel.data_parser import DataParser


class ChatKernel:
    def __init__(self, setup):
        self.connections = self.init_connection_list(setup['connections'])
        self.parse_strip = setup['parse_strip']
        self.outside_request = None
        if setup['method_send_message'] is not None:
            self.send_message = setup['method_send_message']
        if setup['method_close_connection'] is not None:
            self.close_connection = setup['method_close_connection']
        self.version = setup['version']
        self.pack_message = PackMessage(version=self.version)
        self.connections.add_version_header(self.version)
        print(self.pack_message.server_message('start', port=setup['port']))

    @staticmethod
    def init_connection_list(connections):
        return connections if connections is not None else Connected()

    def add_connection(self, connection):
        return self.connections.add_connection(connection, self.version)

    def is_register(self, connection):
        return self.connections.is_register(connection)

    def get_connections(self):
        return self.connections.get_connections()

    def clear_connections(self):
        self.connections.clear_all()

    def get_users(self):
        return self.connections.get_users(self.version)

    def get_name_by_connection(self, connection):
        return self.connections.get_name(connection)

    def get_connection_by_name(self, username):
        return self.connections.get_connection(username)

    def get_connections_by_version(self):
        return self.connections.get_connections_by_version(self.version)

    def get_username_list(self):
        return self.connections.get_username_list()

    def login(self, connection, username):
        return self.connections.register_user(connection, username)

    def set_outside_request(self, func):
        self.outside_request = func

    def prepare_outside(self, req_dict, connection):
        cmd = req_dict.cmd
        param = req_dict.parameter
        body = req_dict.body
        message = ' '.join(req_dict.body) if body is not None else None
        username = self.get_name_by_connection(connection)
        methods = {'login': (self.login_messaging, {'username': param}),
                   'logout': (self.logout_messaging, {'username': username}),
                   'msg': (
                       self.send_message_messaging, {'connection': connection, 'username': param, 'message': message}),
                   'msgall': (self.send_all_messaging, {'connection': connection, 'message': message}),
                   }
        if cmd in ['login', 'logout', 'msg', 'msgall']:
            return methods
        else:
            return -1

    def prepare_run(self, req_dict, connection):
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
        return methods

    def login_messaging(self, username):
        print(self.pack_message.server_message('login', username=username))
        message = self.pack_message.system_message('login', username=username)
        return message

    def logout_messaging(self, username):
        message = self.pack_message.system_message('logout', username=username)
        print(self.pack_message.server_message('logout', username=username))
        return message

    def send_message_messaging(self, connection, username, message):
        sender = self.get_name_by_connection(connection)
        if self.get_connection_by_name(username) is not None:
            message = self.pack_message.chat_message(username=sender, message=message, private=True, target=username)
            return message
        return -12

    def send_all_messaging(self, connection, message):
        sender = self.get_name_by_connection(connection)
        message = self.pack_message.chat_message(username=sender, message=message)
        return message

    def send_all(self, message):
        for user in self.get_users():
            self.send_message(user, message)

    def logout(self, connection):
        self.close_connection(connection)
        self.connections.drop_connection(connection, self.version)

    def from_outside(self, req_dict, connection):
        methods = self.prepare_outside(req_dict, connection)
        if methods != -1:
            cmd = req_dict.cmd
            protocol = ChatProtocol(**methods)
            if cmd == 'msg':
                user = self.get_connection_by_name(req_dict.parameter)
                if user in self.get_connections_by_version():
                    self.send_message(user, protocol.engine(cmd))
            else:
                self.send_all(protocol.engine(cmd))

    def engine(self, request, writer, addr):
        if len(request) > 0:
            if self.add_connection(writer) == 0:
                print(self.pack_message.server_message('new', addr=addr))
            req_dict = DataParser(request, strip=self.parse_strip)
            if req_dict.status == 0:
                if self.outside_request is not None:
                    self.outside_request(req_dict, writer)
                return self.run_command(req_dict, writer)
            else:
                message = self.pack_message.system_error('bad_request', message=req_dict.STATUS_DICT[req_dict.status])
                self.send_message(writer, message)
        elif not request:
            self.logout_engine(writer)
            return -1
        return 0

    def run_command(self, req_dict, connection):
        methods = self.prepare_run(req_dict, connection)
        protocol = ChatProtocol(**methods)
        return protocol.engine(req_dict.cmd)

    def logout_engine(self, connection):
        username = self.get_name_by_connection(connection)
        if username != 0:
            message = self.logout_messaging(username)
            self.logout(connection)
            self.send_all(message)
            return -1

    def login_engine(self, connection, username):
        if self.login(connection, username) == 0:
            message = self.login_messaging(username)
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
        message = self.send_message_messaging(connection, username, message)
        if message != -1:
            user = self.get_connection_by_name(username)
            try:
                self.send_message(user, message)
            except:
                pass
            self.send_message(connection, message)
        else:
            message = self.pack_message.system_error('not_found', username=username)
            self.send_message(connection, message)

    def send_all_engine(self, connection, message):
        message = self.send_all_messaging(connection, message)
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
