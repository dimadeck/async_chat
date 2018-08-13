from base_server.data_parser import DataParser
from base_server.connected import Connected

SERVER_INFO = True
DEBUG_MODE = False


class ChatKernel:
    def __init__(self, connections=None):
        if connections is None:
            self.connections = Connected()
        else:
            self.connections = connections

    def engine(self, request, writer, addr, req_dict):
        if len(request) > 1:

            if DEBUG_MODE:
                print(f'Request: {req_dict.data_list}')  # DEBUG LINE

            if not self.connections.is_exist_connection(writer):
                self.connections.add_connection(writer)
                if SERVER_INFO:
                    print(f"[SERVER INFO] - New connection: {addr}")

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

        if DEBUG_MODE:
            print(f'Command: {cmd}\nParameter: {param}\nBody: {body}')  # DEBUG LINE

        if self.connections.is_register(connection):
            if cmd == 'msg' or cmd == 'msgall':
                self.send_engine(connection, cmd, param, body)
            elif cmd == 'logout':
                self.logout(connection)
                return -1
            elif cmd == 'debug':
                print(self.connections.connections)
                print(self.connections.users)
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

    def send_all(self, message):
        print(self.connections.users)
        for user in self.connections.users.keys():
            self.send_message(user, message)

    def login(self, connection, username):
        if self.connections.register_user(connection, username) == 0:
            self.send_all(f'[System Message]: [{username}] login to chat.')
            if SERVER_INFO:
                print(f'[SERVER INFO] - [{username}] login to chat.')
        else:
            self.send_message(connection, f'[Error]: [{username}]: already exist!')

    def logout(self, connection):
        username = self.connections.get_name(connection)
        connection.close()
        self.connections.drop_connection(connection)
        self.send_all(f'[System Message]: [{username}] logout from chat.')
        if SERVER_INFO:
            print(f'[SERVER INFO] - [{username}] logout from chat.')
