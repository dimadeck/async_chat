from clint.textui import colored

from base_server.connected import Connected
from base_server.data_parser import DataParser
from base_server.logger import Log


class ChatKernel:
    def __init__(self, connections=None, parse_strip='\r\n'):
        self.connections = connections if connections is not None else Connected()
        self.parse_strip = parse_strip
        self.logger = Log()

    def engine(self, request, writer, addr):
        if len(request) > 1:
            req_dict = DataParser(request, strip=self.parse_strip)
            self.logger.log_engine(mode='request', data_list=req_dict.data_list)

            if not self.connections.is_exist_connection(writer):
                self.connections.add_connection(writer)
                self.logger.log_engine(mode='new', addr=addr)

            if req_dict.status == 0:
                if self.run_command(req_dict, writer) == -1:
                    return -1
            else:
                message = self.color_message('error', req_dict.STATUS_DICT[req_dict.status])
                self.send_message(writer, message)
        if not request:
            self.logout(writer)
            return -1
        return 0

    def run_command(self, req_dict, connection):
        cmd = req_dict.cmd
        param = req_dict.parameter
        body = req_dict.body
        self.logger.log_engine(mode='parse', cmd=cmd, param=param, body=body)

        if self.connections.is_register(connection):
            if cmd == 'msg' or cmd == 'msgall':
                self.send_engine(connection, cmd, param, body)
            elif cmd == 'logout':
                self.logout(connection)
                return -1
            elif cmd == 'debug':
                self.logger.log_engine(mess=self.connections.connections)
                self.logger.log_engine(mess=self.connections.users)
            else:
                message = None
                if cmd == 'whoami':
                    message = self.color_message('info', self.connections.get_name(connection))
                elif cmd == 'userlist':
                    message = self.color_message('info', self.connections.get_user_list())
                elif cmd == 'login':
                    message = self.color_message('error', 'Already login!')
                if message is not None:
                    self.send_message(connection, message)
        else:
            if cmd == 'login':
                self.login(connection, param)
            else:
                message = self.color_message('error', 'First login!')
                self.send_message(connection, message)
        return 0

    def send_engine(self, connection, cmd, param, body):
        sender = colored.yellow(self.connections.get_name(connection))
        message = colored.white(' '.join(body))
        if cmd == 'msg':
            user = self.connections.get_connection(param)
            if user is not None:
                self.send_message(user, f'[{sender}*]: {message}')
                self.send_message(connection, f'[{sender}*]: {message}')
            else:
                mess = self.color_message('error', f'[{colored.yellow(user)}]: not found!')
                self.send_message(connection, mess)
        elif cmd == 'msgall':
            self.send_all(f'[{sender}]: {message}')

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
            message = self.color_message('sys', f'[{colored.yellow(username)}] '
                                                f'{colored.green("login to chat.")}')
            self.send_all(message)
            self.logger.log_engine(mode='login', username=username)
        else:
            message = self.color_message('error', f'[{username}]: already exist!')
            self.send_message(connection, message)

    def logout(self, connection):
        username = self.connections.get_name(connection)
        self.close_connection(connection)
        self.connections.drop_connection(connection)
        message = self.color_message('sys', f'[{colored.yellow(username)}] '
                                            f'{colored.red("logout from chat.")}')
        self.send_all(message)
        self.logger.log_engine(mode='logout', username=username)

    def color_message(self, mode, message):
        if mode == 'error':
            message = f'{colored.red("[Error]: ")}{message}'
        elif mode == 'sys':
            message = f'{colored.green("[System Message]: ")}{message}'
        elif mode == 'info':
            message = f'{colored.blue("[INFO]: ")}{message}'
        return message
