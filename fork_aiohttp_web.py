import aiohttp_jinja2
import jinja2
from aiohttp import web

from kernel.fork_chat_kernel import ChatKernel

VERSION = 'aioWSChat'


class AioChat:
    def __init__(self, connections, port):
        self.chat = ChatKernel(connections=connections, parse_strip='', method_send_message=self.send_message,
                               method_close_connection=self.close_connection, version=VERSION, port=port)
        self.app = web.Application()

    def init_app(self):
        aiohttp_jinja2.setup(self.app, loader=jinja2.PackageLoader('view', 'templates'))
        self.app.router.add_get('/', self.index)
        return self.app

    async def index(self, request):
        ws_current = web.WebSocketResponse()
        ws_ready = ws_current.can_prepare(request)
        if not ws_ready.ok:
            return aiohttp_jinja2.render_template('ws_chat.html', request, {'version': VERSION})
        await ws_current.prepare(request)
        while True:
            msg = await ws_current.receive()
            msg = bytes(msg.data, encoding='utf-8')
            if await self.chat.engine(msg, ws_current, 'None') == -1:
                break
        return ws_current

    @staticmethod
    async def send_message(connection, message):
        mes = {'action': 'answer', 'name': message}
        print(mes)
        await connection.send_json(mes)

    @staticmethod
    async def close_connection(connection):
        await connection.close()


def main(port=8080, connections=None):
    server = AioChat(connections, port)
    app = server.init_app()
    web.run_app(app, port=port, host='127.0.0.1')


if __name__ == '__main__':
    main()
