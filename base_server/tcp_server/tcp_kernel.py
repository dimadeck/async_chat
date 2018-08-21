from base_server.base_server import ChatKernel
from base_server.tcp_server.data_parser import DataParser
from chat_pack_message import PackMessage
from chat_protocol import ChatProtocol


class TCPKernel(ChatKernel):
    def __init__(self, connections, parse_strip='\r\n'):
        super(TCPKernel, self).__init__(connections=connections)
        self.parse_strip = parse_strip

    def engine(self, request, writer, addr):
        if len(request) > 1:
            if self.add_connection(writer) == 0:
                print(PackMessage.server_message('new', addr=addr))
            req_dict = DataParser(request, strip=self.parse_strip)
            if req_dict.status == 0:
                return self.run_command(req_dict, writer)
            else:
                message = PackMessage.system_error('bad_request', message=req_dict.STATUS_DICT[req_dict.status])
                self.send_message(writer, message)
        elif not request:
            self.logout_engine(writer)
            return -1
        return 0

    def run_command(self, req_dict, connection):
        cmd = req_dict.cmd
        param = req_dict.parameter
        body = req_dict.body

        if self.is_register(connection):
            methods = {'login': (self.NEW_alredy_login, {'connection': connection}),
                       'logout': (self.logout_engine, {'connection': connection}),
                       'msg': (self.NEW_send_mess, {'connection': connection, 'username': param, 'message': body}),
                       'msgall': (self.NEW_send_all, {'connection': connection, 'message': body}),
                       'debug': (self.NEW_debug, {}),
                       'whoami': (self.NEW_whoami, {'connection': connection}),
                       'userlist': (self.NEW_userlist, {'connection': connection})
                       }
        else:
            methods = {'login': (self.NEW_login, {'connection': connection, 'username': param}),
                       'empty': (self.NEW_first_login, {'connection': connection})}
        protocol = ChatProtocol(**methods)
        return protocol.engine(cmd)

    def logout_engine(self, connection):
        username = self.get_name_by_connection(connection)
        self.logout(connection)
        message = PackMessage.system_message('logout', username=username)
        self.send_all(message)
        return -1

    def NEW_login(self, connection, username):
        if self.login(connection, username) == 0:
            message = PackMessage.system_message('login', username=username)
        else:
            message = PackMessage.system_error('user_exist')
        self.send_all(message)

    def NEW_alredy_login(self, connection):
        message = PackMessage.system_error('already_login')
        self.send_message(connection, message)

    def NEW_first_login(self, connection):
        message = PackMessage.system_error('first_login')
        self.send_message(connection, message)

    def NEW_send_mess(self, connection, username, message):
        sender = self.get_name_by_connection(connection)
        user = self.get_connection_by_name(username)
        message = ' '.join(message)
        if user is not None:
            message = PackMessage.chat_message(username=sender, message=message, private=True)
            self.send_message(user, message)
            self.send_message(connection, message)
        else:
            message = PackMessage.system_error('not_found', username=username)
            self.send_message(connection, message)

    def NEW_send_all(self, connection, message):
        sender = self.get_name_by_connection(connection)
        message = ' '.join(message)
        message = PackMessage.chat_message(username=sender, message=message)
        self.send_all(message)

    def NEW_debug(self):
        connections = ' '.join(self.get_connections())
        userlist = ' '.join(self.get_users())

        print(PackMessage.message(connections))
        print(PackMessage.message(userlist))

    def NEW_whoami(self, connection):
        username = self.get_name_by_connection(connection)
        message = PackMessage.message(username)
        self.send_message(connection, message)

    def NEW_userlist(self, connection):
        userlist = ', '.join(self.get_username_list())
        message = PackMessage.message(userlist)
        self.send_message(connection, message)
