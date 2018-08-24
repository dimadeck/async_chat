import os

from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

from kernel.chat_kernel import ChatKernel

VERSION = "Twisted_WS_Chat"
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
    factory.protocol.chat = ChatKernel(connections=connections, parse_strip='', method_send_message=send_message,
                                       method_close_connection=close_connection, version=VERSION, port=port)

    ws_resource = WebSocketResource(factory)

    root = Resource()
    root.putChild(b"", HttpResource())
    root.putChild(b"ws", ws_resource)

    site = Site(root)
    reactor.listenTCP(port, site)
    reactor.run()


def send_message(connection, message):
    connection.sendMessage(bytes(message, 'utf-8'))


def close_connection(connection):
    connection.sendClose()


if __name__ == '__main__':
    main()
