import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp import web

from base_server.base_server import ChatKernel
from kernel.connected import Connected

VERSION = 'aioChat'


class AioChat(ChatKernel):
    def __init__(self, connections):
        super(AioChat, self).__init__(connections=connections)
        self.app = web.Application()

    def init_app(self):
        self.app.on_shutdown.append(self.shutdown)
        aiohttp_jinja2.setup(self.app, loader=jinja2.PackageLoader('view', 'templates'))
        self.app.router.add_get('/', self.index)
        return self.app

    async def shutdown(self, app):
        try:
            for ws in self.get_users():
                await ws.close()
        except RuntimeError:
            pass
        self.clear_connections()

    async def index(self, request):
        ws_current = web.WebSocketResponse()
        ws_ready = ws_current.can_prepare(request)
        if not ws_ready.ok:
            return aiohttp_jinja2.render_template('index.html', request, {'version': VERSION})
        await ws_current.prepare(request)
        self.add_connection(ws_current)

        name = await self.get_name(ws_current)
        mes = {'action': 'connect', 'name': name}
        await self.send_message(ws_current, mes)

        self.login(ws_current, name)

        mes = {'action': 'join', 'name': name}
        await self.send_all(mes)
        await self.chat_engine(ws_current, name)
        await self.close_connection(ws_current)
        return ws_current

    async def send_all(self, message):
        for user in self.get_users():
            await self.send_message(user, message)

    async def send_message(self, user, message):
        await user.send_json(message)

    async def get_name(self, connection):
        name = await connection.receive()
        return name.data

    async def chat_engine(self, connection, name):
        while True:
            msg = await connection.receive()
            if msg.type == aiohttp.WSMsgType.text:
                mes = {'action': 'sent', 'name': name, 'text': msg.data}
                await self.send_all(mes)
            else:
                break

    async def close_connection(self, connection):
        name = self.get_name_by_connection(connection)
        self.connections.drop_connection(connection)
        mes = {'action': 'disconnect', 'name': name}
        await self.send_all(mes)


def main(port=8080, connections=None):
    if connections is None:
        connections = Connected()
    server = AioChat(connections)
    app = server.init_app()
    web.run_app(app, port=port)


if __name__ == '__main__':
    main()
