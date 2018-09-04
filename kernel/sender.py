from kernel.connected import Connected


class Sender:
    def __init__(self):
        self.connections = Connected()
        self.servers = {}

    def add_server(self, server):
        version = server.VERSION
        self.add_version(version)
        self.servers[version] = server

    def add_version(self, version):
        self.connections.add_version_header(version)

    def add_connection(self, connection, version):
        return self.connections.add_connection(connection, version)

    def is_register(self, connection):
        return self.connections.is_register(connection)

    def get_connections(self):
        return self.connections.get_connections()

    def get_users(self, version):
        return self.connections.get_users(version)

    def get_name_by_connection(self, connection):
        return self.connections.get_name(connection)

    def get_connection_by_name(self, username):
        return self.connections.get_connection(username)

    def get_connections_by_version(self, version):
        return self.connections.get_connections_by_version(version)

    def get_version_by_connection(self, connection):
        return self.connections.get_version_by_connection(connection)

    def get_username_list(self):
        return self.connections.get_username_list()

    def get_register_connections(self):
        return self.connections.get_register_connections()

    def login(self, connection, username):
        return self.connections.register_user(connection, username)

    def drop_connection(self, connection):
        self.connections.drop_connection(connection)

    def send_all(self, message):
        connections = self.get_register_connections()
        for connection in connections:
            self.send(connection, message)

    def send(self, connection, message):
        version = self.get_version_by_connection(connection)
        try:
            self.servers[version].send_message(connection, message)
        except:
            pass

    def close(self, connection):
        version = self.get_version_by_connection(connection)
        self.servers[version].close_connection(connection)

    def logout(self, connection):
        self.close(connection)
        self.drop_connection(connection)
