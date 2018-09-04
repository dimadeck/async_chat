import os

from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

from chats import TwWsServer
from kernel.chat_kernel import ChatKernel
from kernel.sender import Sender

CURRENT_DIR = os.path.dirname(os.path.abspath(__name__))
TEMPLATES_DIR = os.path.join(CURRENT_DIR, 'chats', 'templates')
index = os.path.join(TEMPLATES_DIR, 'index.html')


class HttpResource(Resource):
    def render_GET(self, request):
        html = open(index, "r").read()
        html = html.replace('{{version}}', TwWsServer.VERSION)
        return bytes(html, encoding='utf-8')


class TwistedWsProtocol(WebSocketServerProtocol):
    def onOpen(self):
        print('open')

    def onMessage(self, payload, isBinary):
        request = payload.decode('utf-8').strip('')
        self.chat.engine(request, self, 'None')

    def connectionLost(self, reason):
        print('lost')
        self.chat.logout_engine(self)


class FactoryWS:
    def __init__(self, chat, port):
        self.factory = WebSocketServerFactory(f'ws://127.0.0.1:{port}/ws')
        self.factory.protocol = TwistedWsProtocol

        self.factory.protocol.chat = chat
        self.factory.protocol.chat.add_server(TwWsServer)
        ws_resource = WebSocketResource(self.factory)

        root = Resource()
        root.putChild(b"", HttpResource())
        root.putChild(b"ws", ws_resource)

        self.site = Site(root)


def main(port=8080):
    chat = ChatKernel(TwWsServer, port, sender=Sender())
    server = FactoryWS(chat, port)

    reactor.listenTCP(port, server.site)
    reactor.run()


if __name__ == '__main__':
    main()
