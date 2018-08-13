from clint.textui import colored

from base_server.connected import Connected
from base_server.data_parser import DataParser

SERVER_INFO = True
DEBUG_MODE = False


class ChatKernel:
    def __init__(self, connections=None, parse_strip='\r\n'):
        self.connections = connections if connections is not None else Connected()
        self.parse_strip = parse_strip

    def engine(self, request, writer, addr):
        if len(request) > 1:
            req_dict = DataParser(request, strip=self.parse_strip)
            self.logging(mode='request', data_list=req_dict.data_list)

            if not self.connections.is_exist_connection(writer):
                self.connections.add_connection(writer)
                self.logging(mode='new', addr=addr)

            if req_dict.status == 0:
                if self.run_command(req_dict, writer) == -1:
                    return -1
            else:
                self.send_message(writer, req_dict.STATUS_DICT[req_dict.status])
        if not request:
            self.logout(writer)
            return -1
        return 0

    def run_command(self, req_dict, connection):
        cmd = req_dict.cmd
        param = req_dict.parameter
        body = req_dict.body
        self.logging(mode='parse', cmd=cmd, param=param, body=body)

        if self.connections.is_register(connection):
            if cmd == 'msg' or cmd == 'msgall':
                self.send_engine(connection, cmd, param, body)
            elif cmd == 'logout':
                self.logout(connection)
                return -1
            elif cmd == 'debug':
                self.logging(mess=self.connections.connections)
                self.logging(mess=self.connections.users)
            elif cmd == 'whoami':
                self.send_message(connection, self.connections.get_name(connection))
            elif cmd == 'userlist':
                self.send_message(connection, self.connections.get_user_list())
            elif cmd == 'login':
                self.send_message(connection, '[Error]: Already login!')
        else:
            if cmd == 'login':
                self.login(connection, param)
            else:
                self.send_message(connection, '[Error]: First login!')
        return 0

    def send_engine(self, connection, cmd, param, body):
        sender = self.connections.get_name(connection)
        message = ' '.join(body)
        if cmd == 'msg':
            user = self.connections.get_connection(param)
            if user is not None:
                self.send_message(user, f'[{sender}*]: {message}')
                self.send_message(connection, f'[{sender}*]: {message}')
            else:
                self.send_message(connection, f'[Error]: [{user}]: not found!')
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
            self.send_all(f'[System Message]: [{username}] login to chat.')
            self.logging(mode='login', username=username)
        else:
            self.send_message(connection, f'[Error]: [{username}]: already exist!')

    def logout(self, connection):
        username = self.connections.get_name(connection)
        self.close_connection(connection)
        self.connections.drop_connection(connection)
        self.send_all(f'[System Message]: [{username}] logout from chat.')
        self.logging(mode='logout', username=username)

    @staticmethod
    def logging(mode=None, mess=None, **kwargs):
        if mess is not None:
            print(colored.white(mess))
        if mode is not None:
            message = None
            suffix = None
            color = None
            if SERVER_INFO:
                suffix = '[SERVER INFO] - '
                if mode == 'login':
                    message = f'[{kwargs["username"]}] login to chat.'
                    color = 'green'
                elif mode == 'logout':
                    message = f'[{kwargs["username"]} logout from chat.'
                    color = 'red'
                elif mode == 'new':
                    message = f'New connection: {kwargs["addr"]}'
                    color = 'yellow'
            if DEBUG_MODE:
                suffix = '[DEBUG] - '
                color = 'blue'
                if mode == 'request':
                    message = f'Request: {kwargs["data_list"]}'
                elif mode == 'parse':
                    message = f'Command: {kwargs["cmd"]}\nParameter: {kwargs["param"]}\nBody: {kwargs["body"]}'

            if message is not None:
                if suffix is not None:
                    message = f'{suffix}{message}'
                if color is not None:
                    if color == 'blue':
                        message = colored.blue(message)
                    elif color == 'green':
                        message = colored.green(message)
                    elif color == 'red':
                        message = colored.red(message)
                    elif color == 'yellow':
                        message = colored.yellow(message)
                print(message)
