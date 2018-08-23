class Connected:
    connections = []
    users = {}

    def add_connection(self, connection):
        if not self.is_exist_connection(connection):
            Connected.connections.append(connection)
            return 0
        else:
            return -1

    @staticmethod
    def is_exist_connection(connection):
        return connection in Connected.connections

    @staticmethod
    def is_valid_name(username):
        if username in Connected.users.values():
            return -1
        else:
            return 0

    def register_user(self, connection, username):
        if self.is_valid_name(username) == 0:
            Connected.users[connection] = username
            return 0
        return -1

    @staticmethod
    def is_register(connection):
        return connection in Connected.users

    @staticmethod
    def get_connection(username):
        for connection in Connected.connections:
            if username == Connected.users[connection]:
                return connection
        return None

    @staticmethod
    def get_name(connection):
        try:
            return Connected.users[connection]
        except KeyError:
            return 0

    def drop_connection(self, connection):
        if self.is_register(connection):
            Connected.users.pop(connection)
        if connection in Connected.connections:
            Connected.connections.remove(connection)

    @staticmethod
    def get_username_list():
        user_list = []
        for username in Connected.users.values():
            user_list.append(username)
        return user_list

    @staticmethod
    def get_connections():
        return Connected.connections

    @staticmethod
    def clear_all():
        Connected.connections = []
        Connected.users = {}
