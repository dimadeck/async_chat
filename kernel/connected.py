class Connected:
    connections = []
    users = {}

    @classmethod
    def add_connection(cls, connection):
        if not cls.is_exist_connection(connection):
            cls.connections.append(connection)
            return 0
        else:
            return -1

    @classmethod
    def is_exist_connection(cls, connection):
        return connection in cls.connections

    @classmethod
    def is_valid_name(cls, username):
        if username in cls.users.values():
            return -1
        else:
            return 0

    @classmethod
    def register_user(cls, connection, username):
        if cls.is_valid_name(username) == 0:
            cls.users[connection] = username
            return 0
        return -1

    @classmethod
    def is_register(cls, connection):
        return connection in cls.users

    @classmethod
    def get_connection(cls, username):
        for connection in cls.connections:
            if username == cls.users[connection]:
                return connection
        return None

    @classmethod
    def get_name(cls, connection):
        try:
            return cls.users[connection]
        except KeyError:
            return 0

    @classmethod
    def drop_connection(cls, connection):
        if cls.is_register(connection):
            cls.users.pop(connection)
        if connection in cls.connections:
            cls.connections.remove(connection)

    @classmethod
    def get_username_list(cls):
        user_list = []
        for username in cls.users.values():
            user_list.append(username)
        return user_list

    @classmethod
    def get_connections(cls):
        return cls.connections

    @classmethod
    def clear_all(cls):
        cls.connections = []
        cls.users = {}
