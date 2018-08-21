from base_server.base_server import ChatKernel
from base_server.tcp_server.color_module import ColorServer
from base_server.tcp_server.data_parser import DataParser
from base_server.tcp_server.pack_message import PackMessage
from chat_protocol import ChatProtocol


class TCPKernel(ChatKernel):
    def __init__(self, connections, parse_strip='\r\n'):
        super(TCPKernel, self).__init__(connections=connections)
        self.parse_strip = parse_strip

    def engine(self, request, writer, addr):
        if len(request) > 1:
            if self.add_connection(writer) == 0:
                ColorServer.log_engine(mode='new', addr=addr)

            req_dict = DataParser(request, strip=self.parse_strip)
            ColorServer.log_engine(mode='request', data_list=req_dict.data_list)

            if req_dict.status == 0:
                return self.run_command(req_dict, writer)
            else:
                message = PackMessage.send_response_for_bad_request(req_dict)
                self.send_message(writer, message)
        elif not request:
            self.logout_engine(writer)
            return -1
        return 0

    def run_command(self, req_dict, connection):
        cmd = req_dict.cmd
        param = req_dict.parameter
        body = req_dict.body
        ColorServer.log_engine(mode='parse', cmd=cmd, param=param, body=body)

        if self.is_register(connection):
            methods = {'login': (self.NEW_alredy_login, {'connection': connection}),
                       'logout': (self.logout_engine, {'connection': connection}),
                       'msg': (self.NEW_send_mess, {'connection': connection, 'username': param, 'body': body}),
                       'msgall': (self.NEW_send_all, {'connection': connection, 'body': body}),
                       'debug': (self.NEW_debug, {}),
                       'whoami': (self.NEW_whoami, {'connection': connection}),
                       'userlist': (self.NEW_userlist, {'connection': connection})
                       }
        else:
            methods = {'login': (self.NEW_login, {'connection': connection, 'username': param}),
                       'empty': (self.NEW_first_login, {'connection': connection})}
        protocol = ChatProtocol(**methods)
        return protocol.engine(req_dict.cmd)

    def logout_engine(self, connection):
        username = self.get_name_by_connection(connection)
        self.logout(connection)
        message = PackMessage.send_logout(username)
        self.send_all(message)
        return -1

    def NEW_login(self, connection, username):
        if self.login(connection, username) == 0:
            message = PackMessage.send_success_login(username)
            self.send_all(message)

    def NEW_alredy_login(self, connection):
        message = 'Already login!'
        self.send_message(connection, message)

    def NEW_first_login(self, connection):
        message = PackMessage.send_first_login()
        self.send_message(connection, message)

    def NEW_send_mess(self, connection, username, body):
        sender = self.get_name_by_connection(connection)
        user = self.get_connection_by_name(username)
        if user is not None:
            message = PackMessage.text_message(is_exist=True, sender=sender, body=body)
            self.send_message(user, message)
            self.send_message(connection, message)
        else:
            message = PackMessage.text_message(is_exist=False, username=username)
            self.send_message(connection, message)

    def NEW_send_all(self, connection, body):
        sender = self.get_name_by_connection(connection)
        message = PackMessage.text_message(is_exist=True, private=False, sender=sender, body=body)
        self.send_all(message)

    def NEW_debug(self):
        ColorServer.log_engine(mess=self.get_connections())
        ColorServer.log_engine(mess=self.get_users())

    def NEW_whoami(self, connection):
        username = self.get_name_by_connection(connection)
        message = PackMessage.get_info(cmd='whoami', message=username)
        self.send_message(connection, message)

    def NEW_userlist(self, connection):
        userlist = self.get_username_list()
        message = PackMessage.get_info(cmd='userlist', message=userlist)
        self.send_message(connection, message)
