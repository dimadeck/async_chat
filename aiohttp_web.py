import aiohttp_jinja2
import jinja2
from aiohttp import web

from aiohttp_views import index
from base_server.base_server import ChatKernel
from base_server.connected import Connected


class AioChat(ChatKernel):
    def __init__(self, connections):
        super(AioChat, self).__init__(connections=connections)
        self.app = web.Application()
        self.app['websockets'] = self.connections

    def init_app(self):
        self.app.on_shutdown.append(self.shutdown)
        aiohttp_jinja2.setup(self.app, loader=jinja2.PackageLoader('view', 'templates'))
        self.app.router.add_get('/', index)
        return self.app

    async def shutdown(self, app):
        try:
            for ws in self.app['websockets'].users.keys():
                await ws.close()
        except RuntimeError:
            pass
        app['websockets'].clear_all()


def main(connections=None):
    if connections is None:
        connections = Connected()
    server = AioChat(connections)
    app = server.init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
