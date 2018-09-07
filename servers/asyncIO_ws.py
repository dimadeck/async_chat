import os

from aiohttp import web, WSMsgType

from kernel.fork_chat_kernel import ChatKernel
from kernel.fork_sender import Sender
from servers import AsWsServer

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
STATIC_DIR = os.path.join(TEMPLATES_DIR, 'static')


class AioChat:
    def __init__(self, chat):
        self.chat = chat
        self.app = web.Application()

    def init_app(self):
        self.app.router.add_get('/', lambda index: web.FileResponse(path=os.path.join(TEMPLATES_DIR, 'index.html')))
        self.app.router.add_static('/static', path=STATIC_DIR)
        self.app.router.add_get('/ws', self.ws)
        return self.app

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
