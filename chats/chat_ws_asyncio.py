import aiohttp_jinja2
import jinja2
from aiohttp import web, WSMsgType

from kernel.fork_chat_kernel import ChatKernel

VERSION = 'AsyncIO_WS_Chat'


class AioChat:
    def __init__(self, connections, port):
        self.chat = ChatKernel(connections=connections, parse_strip='', method_send_message=self.send_message,
                               method_close_connection=self.close_connection, version=VERSION, port=port)
        self.app = web.Application()

    def init_app(self):
        aiohttp_jinja2.setup(self.app, loader=jinja2.PackageLoader('chats', 'templates'))
        self.app.router.add_get('/', self.index)
        self.app.router.add_get('/ws', self.ws)
        return self.app

    def index(self, request):
        return aiohttp_jinja2.render_template('index.html', request, {'version': VERSION})

    async def ws(self, request):
        ws_current = web.WebSocketResponse()
        await ws_current.prepare(request)
        while True:
            msg = await ws_current.receive()
            if msg.type == WSMsgType.CLOSE:
                await self.chat.logout_engine(ws_current)
                break
            else:
                msg = bytes(msg.data, encoding='utf-8')
                addr = request.transport.get_extra_info('peername')
                if await self.chat.engine(msg, ws_current, addr) == -1:
                    break
        return ws_current

    @staticmethod
    async def send_message(connection, message):
        mes = {'action': 'response', 'message': message}
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
