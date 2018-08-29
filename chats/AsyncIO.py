import asyncio

import aiohttp_jinja2
import jinja2
from aiohttp import web, WSMsgType

from chats import VERSION_AS, VERSION_AS_WS, get_setup_dict
from kernel.fork_chat_kernel import ChatKernel
from kernel.fork_connected import Connected


class AioChat:
    def __init__(self, connections, port):
        setup_dict = get_setup_dict(connections, VERSION_AS_WS, port)
        self.chat = ChatKernel(setup_dict)
        self.app = web.Application()

    def init_app(self):
        aiohttp_jinja2.setup(self.app, loader=jinja2.PackageLoader('chats', 'templates'))
        self.app.router.add_get('/', self.index)
        self.app.router.add_get('/ws', self.ws)
        return self.app

    def index(self, request):
        return aiohttp_jinja2.render_template('index.html', request, {'version': VERSION_AS_WS})

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


class AsyncioChat:
    def __init__(self, connections, port):
        setup_dict = get_setup_dict(connections, VERSION_AS, port)
        self.chat = ChatKernel(setup_dict)

    async def handle_client(self, reader, writer):
        while True:
            request = (await reader.read(1024))
            addr = writer.get_extra_info('peername')
            if await self.chat.engine(request, writer, addr) == -1:
                break


def main(port1=8000, port2=8080):
    connections = Connected()
    server = AsyncioChat(connections=connections, port=port1)
    server1 = AioChat(connections=connections, port=port2)
    app = server1.init_app()

    server.chat.set_outside_request(server1.chat.from_outside)
    server1.chat.set_outside_request(server.chat.from_outside)

    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(server.handle_client, '127.0.0.1', port1))
    loop.create_task(web.run_app(app, port=port2, host='127.0.0.1'))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()


if __name__ == '__main__':
    main()
