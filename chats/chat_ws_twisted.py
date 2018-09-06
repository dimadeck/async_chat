import os

from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from twisted.internet import reactor
from twisted.web import static
from twisted.web.resource import Resource
from twisted.web.server import Site

from chats import TwWsServer
from kernel.chat_kernel import ChatKernel
from kernel.sender import Sender

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
STATIC_DIR = os.path.join(TEMPLATES_DIR, 'static')


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
        ws_resource = WebSocketResource(self.factory)
        root = Resource()
        root.putChild(b"ws", ws_resource)
        root.putChild(b"static", static.File(STATIC_DIR))
        root.putChild(b"", static.File(os.path.join(TEMPLATES_DIR, 'index.html')))
        self.site = Site(root)


def main(port=8080):
    chat = ChatKernel(TwWsServer, port, sender=Sender())
    server = FactoryWS(chat, port)

    reactor.listenTCP(port, server.site)
    reactor.run()


if __name__ == '__main__':
    main()
