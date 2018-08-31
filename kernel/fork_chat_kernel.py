from kernel.chat_kernel import ChatKernel as CK
from kernel.chat_protocol import ChatProtocol
from kernel.data_parser import DataParser


class ChatKernel(CK):
    async def send(self, connection, message):
        try:
            await self.send_message(connection, message)
        except:
            pass

    async def send_error(self, connection, error_mode, mess=None, username=None):
        message = self.pack_message.system_error(error_mode, message=mess, username=username)
        await self.send(connection, message)

    async def send_info(self, connection, info_mode, clear_data):
        message = self.prepare_info(connection, info_mode, clear_data)
        await self.send(connection, message)

    async def send_all(self, message):
        for user in self.get_users():
            await self.send(user, message)

    async def logout(self, connection):
        await self.close_connection(connection)
        self.connections.drop_connection(connection, self.version)

    async def from_outside(self, req_dict, connection):
        methods = self.prepare_outside(req_dict, connection)
        if methods != -1:
            cmd = req_dict.cmd
            protocol = ChatProtocol(**methods)
            if cmd == 'msg':
                user = self.get_connection_by_name(req_dict.parameter)
                if user in self.get_connections_by_version():
                    await self.send(user, protocol.engine(cmd))
            else:
                await self.send_all(protocol.engine(cmd))

    async def engine(self, request, writer, addr):
        if not request:
            await self.logout_engine(writer)
            return -1
        else:
            req_dict = self.validate_request(request, writer, addr)
            if type(req_dict) == DataParser:
                if self.outside_request is not None:
                    await self.outside_request(req_dict, writer)
                return await self.run_command(req_dict, writer)
            else:
                await self.send_error(writer, 'bad_request', mess=req_dict)
            return 0

    async def run_command(self, req_dict, connection):
        methods = self.prepare_run(req_dict, connection)
        protocol = ChatProtocol(**methods)
        return await protocol.engine(req_dict.cmd)

    async def logout_engine(self, connection):
        username = self.get_name_by_connection(connection)
        if username != 0:
            message = self.logout_messaging(username)
            await self.logout(connection)
            await self.send_all(message)
            return -1

    async def login_engine(self, connection, username):
        if self.login(connection, username) == 0:
            message = self.login_messaging(username)
            await self.send_all(message)
        else:
            await self.send_error(connection, 'user_exist')

    async def send_message_engine(self, connection, username, message):
        message = self.send_message_messaging(connection, username, message)
        if message != -1:
            user = self.get_connection_by_name(username)
            await self.send(user, message)
            await self.send(connection, message)
        else:
            await self.send_error(connection, 'not_found', username=username)

    async def send_all_engine(self, connection, message):
        message = self.send_all_messaging(connection, message)
        await self.send_all(message)

    async def debug_engine(self):
        connections = self.get_connections()
        userlist = self.get_users()

        print(self.pack_message.message(connections))
        print(self.pack_message.message(userlist))
