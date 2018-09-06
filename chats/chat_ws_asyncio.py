import aiohttp_jinja2
import jinja2
from aiohttp import web, WSMsgType

from chats import AsWsServer
from kernel.fork_chat_kernel import ChatKernel
from kernel.fork_sender import Sender


class AioChat:
    def __init__(self, chat):
        self.chat = chat
        self.app = web.Application()

    def init_app(self):
        aiohttp_jinja2.setup(self.app, loader=jinja2.PackageLoader('chats', 'templates'))
        self.app.router.add_get('/', self.index)
        self.app.router.add_get('/ws', self.ws)
        return self.app

    def index(self, request):
        return aiohttp_jinja2.render_template('index.html', request, {})

    async def ws(self, request):

        ws_current = web.WebSocketResponse()
        await ws_current.prepare(request)
        while True:
            try:
                msg = await ws_current.receive()
                if msg.type == WSMsgType.CLOSE:
                    await self.chat.logout_engine(ws_current)
                    break
                else:
                    msg = bytes(msg.data, encoding='utf-8')
                    addr = request.transport.get_extra_info('peername')
                    req = msg.decode('utf-8').strip('')
                    if await self.chat.engine(req, ws_current, addr) == -1:
                        break
            except:
                break
        return ws_current


def main(port=8080):
    chat = ChatKernel(AsWsServer, port, sender=Sender())
    server = AioChat(chat)
    app = server.init_app()
    web.run_app(app, port=port, host='127.0.0.1')


if __name__ == '__main__':
    main()
