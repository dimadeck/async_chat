from kernel.chat_pack_message import PackMessage
from kernel.chat_protocol import ChatProtocol
from kernel.data_parser import DataParser


class ChatKernel:
    def __init__(self, server, port, sender):
        self.version = server.VERSION
        self.sender = sender
        self.sender.add_server(server)
        print(PackMessage.server_message(server_mode='start', port=port, version=self.version))

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
                       'whoami': (self.send_info, {'connection': connection, 'info_mode': 'whoami',
                                                   'clear_data': req_dict.clear_data,
                                                   'username': self.sender.get_name_by_connection(connection)}),
                       'userlist': (self.send_info, {'connection': connection, 'clear_data': req_dict.clear_data,
                                                     'userlist': self.sender.get_username_list(),
                                                     'info_mode': 'userlist'})
                       }
        else:
            methods = {'login': (self.login_engine, {'connection': connection, 'username': param}),
                       'empty': (self.send_error, {'connection': connection, 'error_mode': 'first_login'})}
        return methods

    def validate_request(self, request, connection, addr):
        if self.sender.add_connection(connection, self.version) == 0:
            print(PackMessage.server_message('new', addr=addr, version=self.version))
        req_dict = DataParser(request)
        if req_dict.status == 0:
            return req_dict
        else:
            return req_dict.STATUS_DICT[req_dict.status]

    def send_error(self, connection, error_mode, mess=None, username=None):
        message = PackMessage.prepare_message('error', error_mode=error_mode, message=mess, username=username)
        self.sender.send(connection, message)

    def send_info(self, connection, info_mode, clear_data, userlist=None, username=None):
        message = PackMessage.prepare_message('info', info_mode=info_mode, clear_data=clear_data,
                                              userlist=userlist, username=username)
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

    def login_engine(self, connection, username):
        if self.sender.login(connection, username) == 0:
            message = PackMessage.prepare_message(mode='login', username=username, version=self.version)
            self.sender.send_all(message)
        else:
            self.send_error(connection, 'user_exist')

    def logout_engine(self, connection):
        username = self.sender.get_name_by_connection(connection)
        if username != 0:
            message = PackMessage.prepare_message(mode='logout', username=username, version=self.version)
            self.sender.send_all(message)
            self.sender.logout(connection)

    def send_message_engine(self, connection, username, message):
        user = self.sender.get_connection_by_name(username)
        if user is not None:
            message = PackMessage.prepare_message(mode='send_message', username=username, message=message,
                                                  sender=self.sender.get_name_by_connection(connection))
            self.sender.send(user, message)
            self.sender.send(connection, message)
        else:
            self.send_error(connection, 'not_found', username=username)

    def send_all_engine(self, connection, message):
        username = self.sender.get_name_by_connection(connection)
        message = PackMessage.prepare_message(mode='send_message_all', username=username, message=message)
        self.sender.send_all(message)
