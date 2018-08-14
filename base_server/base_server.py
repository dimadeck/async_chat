from base_server.color_module import Color, ColorChat, ColorServer
from base_server.connected import Connected
from base_server.data_parser import DataParser


class ChatKernel:
    def __init__(self, connections=None, parse_strip='\r\n'):
        self.connections = connections if connections is not None else Connected()
        self.parse_strip = parse_strip

    def engine(self, request, writer, addr):
        if len(request) > 1:
            req_dict = DataParser(request, strip=self.parse_strip)
            ColorServer.log_engine(mode='request', data_list=req_dict.data_list)
            self.add_connection(writer, addr)

            if req_dict.status == 0:
                return self.run_command(req_dict, writer)
            else:
                self.response_for_bad_request(req_dict, writer)
        if not request:
            self.logout(writer)
            return -1
        return 0

    def add_connection(self, connection, addr):
        if not self.connections.is_exist_connection(connection):
            self.connections.add_connection(connection)
            ColorServer.log_engine(mode='new', addr=addr)

    def response_for_bad_request(self, req_dict, connection):
        message = req_dict.STATUS_DICT[req_dict.status]
        message = ColorChat.add_suffix('error', message)
        self.send_message(connection, message)

    def run_command(self, req_dict, connection):
        cmd = req_dict.cmd
        param = req_dict.parameter
        body = req_dict.body
        ColorServer.log_engine(mode='parse', cmd=cmd, param=param, body=body)

        if self.connections.is_register(connection):
            if cmd == 'msg' or cmd == 'msgall':
                self.send_engine(connection, cmd, param, body)
            elif cmd == 'logout':
                self.logout(connection)
                return -1
            elif cmd == 'debug':
                ColorServer.log_engine(mess=self.connections.connections)
                ColorServer.log_engine(mess=self.connections.users)
            else:
                message = None
                if cmd == 'whoami':
                    message = self.connections.get_name(connection)
                    message = ColorChat.add_suffix('info', message)
                elif cmd == 'userlist':
                    message = self.connections.get_user_list()
                    message = ColorChat.add_suffix('info', message)
                elif cmd == 'login':
                    message = 'Already login!'
                    message = ColorChat.add_suffix('error', message)
                if message is not None:
                    self.send_message(connection, message)
        else:
            if cmd == 'login':
                self.login(connection, param)
            else:
                message = 'First login!'
                message = ColorChat.add_suffix('error', message)
                self.send_message(connection, message)
        return 0

    def send_engine(self, connection, cmd, param, body):
        sender = self.connections.get_name(connection)
        message = ' '.join(body)

        sender = ColorChat.color_user(sender)
        message = ColorChat.color_message(message)

        if cmd == 'msg':
            username = param
            user = self.connections.get_connection(username)
            if user is not None:
                message = f'[{sender}*]: {message}'
                self.send_message(user, message)
                self.send_message(connection, message)
            else:
                message = 'not found!'
                username = ColorChat.color_user(username)
                message = ColorChat.add_suffix('error', f'[{username}]: {message}')
                self.send_message(connection, message)
        elif cmd == 'msgall':
            message = f'[{sender}]: {message}'
            self.send_all(message)

    @staticmethod
    def send_message(connection, message):
        raise NotImplementedError

    @staticmethod
    def close_connection(connection):
        raise NotImplementedError

    def send_all(self, message):
        for user in self.connections.users.keys():
            self.send_message(user, message)

    def login(self, connection, username):

        if self.connections.register_user(connection, username) == 0:

            ColorServer.log_engine(mode='login', username=username)
            message = "login to chat."
            message = Color.change_color('green', message)

            username = ColorChat.color_user(username)

            message = f'[{username}] {message}'
            message = ColorChat.add_suffix('sys', message)

            self.send_all(message)

        else:
            username = ColorChat.color_user(username)
            message = 'already exist!'
            message = f'[{username}]: {message}'
            message = ColorChat.add_suffix('error', message)

            self.send_message(connection, message)

    def logout(self, connection):
        username = self.connections.get_name(connection)

        ColorServer.log_engine(mode='logout', username=username)

        message = "logout from chat."
        message = Color.change_color('red', message)
        username = ColorChat.color_user(username)
        message = f'[{username}] {message}'
        message = ColorChat.add_suffix('sys', message)
        self.close_connection(connection)
        self.connections.drop_connection(connection)

        self.send_all(message)
