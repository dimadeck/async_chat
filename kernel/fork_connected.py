class Connected:
    connections = []
    users = {}

    def add_connection(self, connection):
        if not self.is_exist_connection(connection):
            Connected.connections.append(connection)
            return 0
        else:
            return -1

    def is_exist_connection(self, connection):
        return connection in Connected.connections

    def is_valid_name(self, username):
        if username in Connected.users.values():
            return -1
        else:
            return 0

    def register_user(self, connection, username):
        if self.is_valid_name(username) == 0:
            Connected.users[connection] = username
            return 0
        return -1

    def is_register(self, connection):
        return connection in Connected.users

    def get_connection(self, username):
        for connection in Connected.connections:
            if username == Connected.users[connection]:
                return connection
        return None

    def get_name(self, connection):
        try:
            return Connected.users[connection]
        except KeyError:
            return 0

    def drop_connection(self, connection):
        if self.is_register(connection):
            Connected.users.pop(connection)
        if connection in Connected.connections:
            Connected.connections.remove(connection)

    def get_username_list(self):
        user_list = []
        for username in Connected.users.values():
            user_list.append(username)
        return user_list

    def get_connections(self):
        return Connected.connections

    def clear_all(self):
        Connected.connections = []
        Connected.users = {}

