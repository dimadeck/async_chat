from kernel.chat_pack_message import PackMessage
from kernel.chat_protocol import ChatProtocol
from kernel.data_parser import DataParser


class ChatKernel:
    def __init__(self, server, port, sender):
        self.version = server.VERSION
        self.pack_message = PackMessage(version=self.version)
        self.sender = sender
        print(self.pack_message.server_message('start', port=port))

    def add_server(self, server):
        self.sender.add_server(server)

    def prepare_run(self, req_dict, connection):
        param = req_dict.parameter
        body = req_dict.body
        message = ' '.join(req_dict.body) if body is not None else None

        if self.sender.is_register(connection):
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
        sender = self.sender.get_name_by_connection(connection)
        if self.sender.get_connection_by_name(username) is not None:
            message = self.pack_message.chat_message(username=sender, message=message, private=True, target=username)
            return message
        else:
            return -1

    def send_all_messaging(self, connection, message):
        sender = self.sender.get_name_by_connection(connection)
        message = self.pack_message.chat_message(username=sender, message=message)
        return message

    def prepare_info(self, connection, info_mode, clear_data):
        info_set = {'whoami': self.sender.get_name_by_connection(connection),
                    'userlist': self.sender.get_username_list()}
        message = self.pack_message.system_info(info_set[info_mode], clear_data)
        return message

    def prepare_debug(self):
        connections = self.sender.get_connections()
        userlist = self.sender.get_users(self.version)

        print(self.pack_message.message(connections))
        print(self.pack_message.message(userlist))

    def validate_request(self, request, connection, addr):
        if self.sender.add_connection(connection, self.version) == 0:
            print(self.pack_message.server_message('new', addr=addr))
        req_dict = DataParser(request)
        if req_dict.status == 0:
            return req_dict
        else:
            return req_dict.STATUS_DICT[req_dict.status]

    def send_error(self, connection, error_mode, mess=None, username=None):
        message = self.pack_message.system_error(error_mode, message=mess, username=username)
        self.sender.send(connection, message)

    def send_info(self, connection, info_mode, clear_data):
        message = self.prepare_info(connection, info_mode, clear_data)
        self.sender.send(connection, message)

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
        return state

    def logout_engine(self, connection):
        username = self.sender.get_name_by_connection(connection)
        if username != 0:
            message = self.logout_messaging(username)
            self.sender.send_all(message)
            self.sender.logout(connection)
            return -1

    def login_engine(self, connection, username):
        if self.sender.login(connection, username) == 0:
            message = self.login_messaging(username)
            self.sender.send_all(message)
            return 0
        else:
            self.send_error(connection, 'user_exist')
            return -10

    def send_message_engine(self, connection, username, message):
        message = self.send_message_messaging(connection, username, message)
        if message != -1:
            user = self.sender.get_connection_by_name(username)
            self.sender.send(user, message)
            self.sender.send(connection, message)
            return 0
        else:
            self.send_error(connection, 'not_found', username=username)
            return -10

    def send_all_engine(self, connection, message):
        message = self.send_all_messaging(connection, message)
        self.sender.send_all(message)
        return 0

    def debug_engine(self):
        self.prepare_debug()
