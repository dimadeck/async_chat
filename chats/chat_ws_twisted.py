import os

from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

from chats import VERSION_TW_WS as VERSION, get_setup_dict
from kernel.chat_kernel import ChatKernel

CURRENT_DIR = os.path.dirname(os.path.abspath(__name__))
TEMPLATES_DIR = os.path.join(CURRENT_DIR, 'chats', 'templates')
index = os.path.join(TEMPLATES_DIR, 'index.html')


class HttpResource(Resource):
    def render_GET(self, request):
        html = open(index, "r").read()
        html = html.replace('{{version}}', VERSION)
        return bytes(html, encoding='utf-8')


class TwistedWsProtocol(WebSocketServerProtocol):
    def onOpen(self):
        print('open')

    def onMessage(self, payload, isBinary):
        self.chat.engine(payload, self, 'None')

    def connectionLost(self, reason):
        print('lost')
        self.chat.logout_engine(self)


def main(connections=None, port=1234):
    factory = WebSocketServerFactory(f'ws://127.0.0.1:{port}/ws')
    factory.protocol = TwistedWsProtocol
    setup_dict = get_setup_dict(connections, VERSION, port)
    factory.protocol.chat = ChatKernel(setup_dict)
    ws_resource = WebSocketResource(factory)

    root = Resource()
    root.putChild(b"", HttpResource())
    root.putChild(b"ws", ws_resource)

    site = Site(root)
    reactor.listenTCP(port, site)
    reactor.run()


if __name__ == '__main__':
    main()
