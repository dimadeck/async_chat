from base_server.connected import Connected


class ChatKernel:
    def __init__(self, connections=None):
        self.connections = self.init_connection_list(connections)

    @staticmethod
    def init_connection_list(connections):
        return connections if connections is not None else Connected()

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

    def logout(self, connection):
        self.close_connection(connection)
        self.connections.drop_connection(connection)

    def add_connection(self, connection):
        return self.connections.add_connection(connection)

    def is_register(self, connection):
        return self.connections.is_register(connection)

    def get_connections(self):
        return self.connections.connections

    def get_users(self):
        return self.connections.users

    def get_name_by_connection(self, connection):
        return self.connections.get_name(connection)

    def get_connection_by_name(self, username):
        return self.connections.get_connection(username)

    def get_username_list(self):
        return self.connections.get_username_list()
