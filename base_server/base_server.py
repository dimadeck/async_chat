from base_server.color_module import ColorServer
from base_server.connected import Connected
from base_server.data_parser import DataParser
from base_server.pack_message import PackMessage


class ChatKernel:
    def __init__(self, connections=None, parse_strip='\r\n'):
        self.connections = connections if connections is not None else Connected()
        self.parse_strip = parse_strip

    def engine(self, request, writer, addr):
        if len(request) > 1:
            req_dict = DataParser(request, strip=self.parse_strip)
            ColorServer.log_engine(mode='request', data_list=req_dict.data_list)
            if self.connections.add_connection(writer) == 0:
                ColorServer.log_engine(mode='new', addr=addr)

            if req_dict.status == 0:
                return self.run_command(req_dict, writer)
            else:
                message = PackMessage.send_response_for_bad_request(req_dict)
                self.send_message(writer, message)
        if not request:
            self.logout_engine(writer)
            return -1
        return 0

    def run_command(self, req_dict, connection):
        cmd = req_dict.cmd
        param = req_dict.parameter
        body = req_dict.body
        ColorServer.log_engine(mode='parse', cmd=cmd, param=param, body=body)

        if self.connections.is_register(connection):
            if cmd == 'msg' or cmd == 'msgall':
                self.send_engine(connection, cmd, param, body)
            elif cmd == 'logout':
                self.logout_engine(connection)
                return -1
            elif cmd == 'debug':
                ColorServer.log_engine(mess=self.connections.connections)
                ColorServer.log_engine(mess=self.connections.users)
            else:
                message = None
                if cmd == 'whoami':
                    username = self.connections.get_name(connection)
                    message = PackMessage.get_info(cmd='whoami', message=username)
                elif cmd == 'userlist':
                    userlist = self.connections.get_user_list()
                    message = PackMessage.get_info(cmd='userlist', message=userlist)
                elif cmd == 'login':
                    message = PackMessage.get_info(cmd='login')
                self.send_message(connection, message)
        else:
            if cmd == 'login':
                if self.login(connection, param) == 0:
                    message = PackMessage.send_success_login(param)
                    self.send_all(message)
                else:
                    message = PackMessage.send_already_login(param)
                    self.send_message(connection, message)
            else:
                message = PackMessage.send_first_login()
                self.send_message(connection, message)
        return 0

    def send_engine(self, connection, cmd, username, body):
        sender = self.connections.get_name(connection)
        if cmd == 'msg':
            user = self.connections.get_connection(username)
            if user is not None:
                message = PackMessage.text_message(is_exist=True, sender=sender, body=body)
                self.send_message(user, message)
                self.send_message(connection, message)
            else:
                message = PackMessage.text_message(is_exist=False, username=username)
                self.send_message(connection, message)
        elif cmd == 'msgall':
            message = PackMessage.text_message(is_exist=True, private=False, sender=sender, body=body)
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
        return self.connections.register_user(connection, username)

    def logout_engine(self, connection):
        username = self.connections.get_name(connection)
        self.logout(connection)
        message = PackMessage.send_logout(username)
        self.send_all(message)

    def logout(self, connection):
        self.close_connection(connection)
        self.connections.drop_connection(connection)
