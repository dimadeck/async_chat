import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp import web

from base_server.base_server import ChatKernel
from base_server.connected import Connected

VERSION = 'aioChat'


class AioChat(ChatKernel):
    def __init__(self, connections):
        super(AioChat, self).__init__(connections=connections)
        self.app = web.Application()
        self.app['websockets'] = self.connections

    def init_app(self):
        self.app.on_shutdown.append(self.shutdown)
        aiohttp_jinja2.setup(self.app, loader=jinja2.PackageLoader('view', 'templates'))
        self.app.router.add_get('/', self.index)
        return self.app

    async def shutdown(self, app):
        try:
            # for ws in self.connections.users.keys():
            for ws in self.app['websockets'].users.keys():
                await ws.close()
        except RuntimeError:
            pass
        # self.connections.clear_all()
        app['websockets'].clear_all()

    ##

    async def index(self, request):
        ws_current = web.WebSocketResponse()
        ws_ready = ws_current.can_prepare(request)
        if not ws_ready.ok:
            return aiohttp_jinja2.render_template('index.html', request, {'version': VERSION})
        await ws_current.prepare(request)
        name = await self.get_name(ws_current)
        await self.send_mess(ws_current, action='connect', name=name)

        request.app['websockets'].add_connection(ws_current)
        request.app['websockets'].register_user(ws_current, name)

        # self.connections.add_connection(ws_current)
        self.login(ws_current, name)

        mes = {'action': 'join', 'name': name}
        await self.send_al(request, action='join', name=name)
        # await self.send_all(mes)
        # await self.chat_engine(ws_current, name)
        await self.chat_engine(request, ws_current, name)
        await self.close_connect(request, ws_current, name)
        return ws_current

    async def send_message(self, user, kwargs):
        await user.send_json(kwargs)

    async def send_mess(self, user, **kwargs):
        await user.send_json(kwargs)

    async def send_al(self, request, **kwargs):
        # for user in self.connections.users.keys():
        for user in request.app['websockets'].users.keys():
            await self.send_mess(user, **kwargs)

    async def get_name(self, connection):
        name = await connection.receive()
        return name.data

    async def chat_engine(self, request, connection, name):
        # async def chat_engine(self, connection, name):

        while True:
            msg = await connection.receive()
            if msg.type == aiohttp.WSMsgType.text:
                # mes = {'action': 'sent', 'name': name, 'text': msg.data}
                # await self.send_all(mes)

                mes = {'action': 'sent', 'name': name, 'text': msg.data}
                await self.send_al(request, action='sent', name=name, text=msg.data)
            else:
                break

    async def close_connect(self,request, connection, name):
#    async def close_connect(self,connection, name):

        self.connections.drop_connection(connection)
        mes = {'action': 'disconnect', 'name': name}
        await self.send_al(request, action='disconnect', name=name)
        # await self.send_all(mes)


##

def main(connections=None):
    if connections is None:
        connections = Connected()
    server = AioChat(connections)
    app = server.init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
