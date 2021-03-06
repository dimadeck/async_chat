class Connected:
    def __init__(self):
        self.connections_list = []
        self.connections = {}
        self.users = {}

    def add_version_header(self, version):
        if version not in self.connections:
            self.connections[version] = []
            return 0
        return -1

    def add_connection(self, connection, version):
        if not self.is_exist_connection(connection):
            self.connections_list.append(connection)
            try:
                self.connections[version].append(connection)
            except KeyError:
                return -2
            return 0
        else:
            return -1

    def get_connections_by_version(self, version):
        return self.connections[version]

    def get_version_by_connection(self, connection):
        if connection in self.connections_list:
            for version in self.connections:
                if connection in self.connections[version]:
                    return version
            return -1
        else:
            return -2

    def is_exist_connection(self, connection):
        return connection in self.connections_list

    def is_valid_name(self, username):
        if username in self.users.values() or username == '':
            return -1
        else:
            return 0

    def register_user(self, connection, username):
        if self.is_valid_name(username) == 0:
            if connection in self.connections_list:
                self.users[connection] = username
                return 0
            else:
                return -2
        return -1

    def is_register(self, connection):
        return connection in self.users

    def get_connection(self, username):
        for connection, user in self.users.items():
            if user == username:
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
        if connection in self.connections_list:
            version = self.get_version_by_connection(connection)
            self.connections[version].remove(connection)
            self.connections_list.remove(connection)

    def get_username_list(self):
        user_list = []
        for username in self.users.values():
            user_list.append(username)
        return user_list

    def get_connections(self):
        return self.connections_list

    def get_register_connections(self):
        register_list = []
        for connection in self.users:
            register_list.append(connection)
        return register_list

    def get_users(self, version):
        user_list = {}
        for connection, username in self.users.items():
            if connection in self.connections[version]:
                user_list[connection] = username
        return user_list

    def clear_all(self):
        self.connections_list = []
        self.connections = {}
        self.users = {}
