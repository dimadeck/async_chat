from kernel.chat_kernel import ChatKernel as CK
from kernel.chat_pack_message import PackMessage
from kernel.chat_protocol import ChatProtocol
from kernel.data_parser import DataParser


class ChatKernel(CK):
    async def send_error(self, connection, error_mode, mess=None, username=None):
        message = PackMessage.prepare_message('error', error_mode=error_mode, message=mess, username=username)
        await self.sender.send(connection, message)

    async def send_info(self, connection, info_mode, clear_data, userlist=None, username=None):
        message = PackMessage.prepare_message('info', info_mode=info_mode, clear_data=clear_data,
                                              userlist=userlist, username=username)
        await self.sender.send(connection, message)

    async def engine(self, request, writer, addr):
        if not request:
            await self.logout_engine(writer)
            return -1
        else:
            req_dict = self.validate_request(request, writer, addr)
            if type(req_dict) == DataParser:
                return await self.run_command(req_dict, writer)
            else:
                await self.send_error(writer, 'bad_request', mess=req_dict)
            return 0

    async def run_command(self, req_dict, connection):
        methods = self.prepare_run(req_dict, connection)
        protocol = ChatProtocol(**methods)
        state = await protocol.engine(req_dict.cmd)
        return state

    async def login_engine(self, connection, username):
        if self.sender.login(connection, username) == 0:
            message = PackMessage.prepare_message(mode='login', username=username, version=self.version)
            await self.sender.send_all(message)
        else:
            await self.send_error(connection, 'user_exist')

    async def logout_engine(self, connection):
        username = self.sender.get_name_by_connection(connection)
        if username != 0:
            message = PackMessage.prepare_message(mode='logout', username=username, version=self.version)
            await self.sender.send_all(message)
            await self.sender.logout(connection)

    async def send_message_engine(self, connection, username, message):
        user = self.sender.get_connection_by_name(username)
        if user is not None:
            message = PackMessage.prepare_message(mode='send_message', username=username, message=message,
                                                  sender=self.sender.get_name_by_connection(connection))
            await self.sender.send(user, message)
            await self.sender.send(connection, message)
        else:
            await self.send_error(connection, 'not_found', username=username)

    async def send_all_engine(self, connection, message):
        username = self.sender.get_name_by_connection(connection)
        message = PackMessage.prepare_message(mode='send_message_all', username=username, message=message)
        await self.sender.send_all(message)
