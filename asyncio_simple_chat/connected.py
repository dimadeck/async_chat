class Connected:
    def __init__(self):
        self.connections = []
        self.users = {}

    def add_connection(self, connection):
        self.connections.append(connection)

    def is_valid_name(self, username):
        if username in self.users.values():
            return -1
        else:
            return 0

    def register_user(self, connection, username):
        self.users[connection] = username

    def is_register(self, connection):
        return connection in self.users

    def get_connection(self, username):
        for connection in self.connections:
            if username == self.users[connection]:
                return connection
        return None

    def get_name(self, connection):
        try:
            return self.users[connection]
        except KeyError:
            return 0

    def drop_connection(self, connection):
        if self.is_register(connection):
            self.users.pop(connection)
        if connection in self.connections:
            self.connections.remove(connection)

    def get_user_list(self):
        user_list = []
        for username in self.users.values():
            user_list.append(username)
        return user_list

    def get_connections(self):
        return self.connections