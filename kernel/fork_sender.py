from kernel.sender import Sender as S


class Sender(S):
    async def send_all(self, message):
        connections = self.get_register_connections()
        for connection in connections:
            await self.send(connection, message)

    async def send(self, connection, message):
        version = self.get_version_by_connection(connection)
        try:
            await self.servers[version].send_message(connection, message)
        except:
            pass

    async def close(self, connection):
        version = self.get_version_by_connection(connection)
        await self.servers[version].close_connection(connection)

    async def logout(self, connection):
        await self.close(connection)
        self.drop_connection(connection)
