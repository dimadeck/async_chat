from kernel.chat_pack_message import PackMessage
from kernel.chat_protocol import ChatProtocol
from kernel.connected import Connected
from kernel.data_parser import DataParser


class ChatKernel:
    def __init__(self, setup):
        self.connections = self.init_connection_list(setup['connections'])
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
        if cmd in ['login', 'logout', 'msg', 'msgall']:
            param = req_dict.parameter
            body = req_dict.body
            message = ' '.join(req_dict.body) if body is not None else None
            username = self.get_name_by_connection(connection)
            methods = {'login': (self.login_messaging, {'username': param}),
                       'logout': (self.logout_messaging, {'username': username}),
                       'msg': (
                           self.send_message_messaging,
                           {'connection': connection, 'username': param, 'message': message}),
                       'msgall': (self.send_all_messaging, {'connection': connection, 'message': message}),
                       }
            return methods
        else:
            return -1

    def prepare_run(self, req_dict, connection):
        param = req_dict.parameter
        body = req_dict.body
        message = ' '.join(req_dict.body) if body is not None else None

        if self.is_register(connection):
            methods = {'login': (self.send_error, {'connection': connection, 'error_mode': 'already_login'}),
                       'logout': (self.logout_engine, {'connection': connection}),
                       'msg': (
                           self.send_message_engine, {'connection': connection, 'username': param, 'message': message}),
                       'msgall': (self.send_all_engine, {'connection': connection, 'message': message}),
                       'debug': (self.debug_engine, {}),
                       'whoami': (self.send_info,
                                  {'connection': connection, 'info_mode': 'whoami', 'clear_data': req_dict.clear_data}),
                       'userlist': (self.send_info, {'connection': connection, 'info_mode': 'userlist',
                                                     'clear_data': req_dict.clear_data})
                       }
        else:
            methods = {'login': (self.login_engine, {'connection': connection, 'username': param}),
                       'empty': (self.send_error, {'connection': connection, 'error_mode': 'first_login'})}
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
        else:
            return -1

    def send_all_messaging(self, connection, message):
        sender = self.get_name_by_connection(connection)
        message = self.pack_message.chat_message(username=sender, message=message)
        return message

    def prepare_info(self, connection, info_mode, clear_data):
        if clear_data and 'WS' in self.version:
            info_set = {'whoami': self.get_name_by_connection(connection),
                        'userlist': self.get_username_list()}
            message = self.pack_message.system_info(info_set[info_mode], clear_data)
        else:
            info_set = {'whoami': self.get_name_by_connection(connection),
                        'userlist': ', '.join(self.get_username_list())}
            message = self.pack_message.system_info(info_set[info_mode], clear_data)
        return message

    def prepare_debug(self):
        connections = self.get_connections()
        userlist = self.get_users()

        print(self.pack_message.message(connections))
        print(self.pack_message.message(userlist))

    def validate_request(self, request, connection, addr):
        if self.add_connection(connection) == 0:
            print(self.pack_message.server_message('new', addr=addr))
        req_dict = DataParser(request)
        if req_dict.status == 0:
            return req_dict
        else:
            return req_dict.STATUS_DICT[req_dict.status]

    def send(self, connection, message):
        try:
            self.send_message(connection, message)
        except:
            pass

    def send_error(self, connection, error_mode, mess=None, username=None):
        message = self.pack_message.system_error(error_mode, message=mess, username=username)
        self.send(connection, message)

    def send_info(self, connection, info_mode, clear_data):
        message = self.prepare_info(connection, info_mode, clear_data)
        self.send(connection, message)

    def send_all(self, message):
        for user in self.get_users():
            self.send(user, message)

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
                    self.send(user, protocol.engine(cmd))
            else:
                self.send_all(protocol.engine(cmd))

    def engine(self, request, writer, addr):
        if not request:
            self.logout_engine(writer)
            return -1
        else:
            req_dict = self.validate_request(request, writer, addr)
            if type(req_dict) == DataParser:
                return self.run_command(req_dict, writer)
            else:
                self.send_error(writer, 'bad_request', mess=req_dict)
            return 0

    def run_command(self, req_dict, connection):
        methods = self.prepare_run(req_dict, connection)
        protocol = ChatProtocol(**methods)
        state = protocol.engine(req_dict.cmd)
        if state == 0:
            if self.outside_request is not None:
                self.outside_request(req_dict, connection)
        return state

    def logout_engine(self, connection):
        username = self.get_name_by_connection(connection)
        if username != 0:
            message = self.logout_messaging(username)
            if self.outside_request is not None:
                self.outside_request(DataParser('logout'), connection)
            self.send_all(message)
            self.logout(connection)
            return -1

    def login_engine(self, connection, username):
        if self.login(connection, username) == 0:
            message = self.login_messaging(username)
            self.send_all(message)
            return 0
        else:
            self.send_error(connection, 'user_exist')
            return -10

    def send_message_engine(self, connection, username, message):
        message = self.send_message_messaging(connection, username, message)
        if message != -1:
            user = self.get_connection_by_name(username)
            self.send(user, message)
            self.send(connection, message)
            return 0
        else:
            self.send_error(connection, 'not_found', username=username)
            return -10

    def send_all_engine(self, connection, message):
        message = self.send_all_messaging(connection, message)
        self.send_all(message)
        return 0

    def debug_engine(self):
        self.prepare_debug()
