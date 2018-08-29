from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

from chats import get_setup_dict, VERSION_TW_WS
from chats.chat_twisted import Factory
from chats.chat_ws_twisted import TwistedWsProtocol, HttpResource
from kernel.chat_kernel import ChatKernel


def main(port1=8000, port2=8080, connections=None):
    server1 = Factory(connections=connections, port=port1)
    reactor.listenTCP(port1, server1)

    factory = WebSocketServerFactory(f'ws://127.0.0.1:{port2}/ws')
    factory.protocol = TwistedWsProtocol
    setup_dict = get_setup_dict(server1.chat.connections, VERSION_TW_WS, port2)
    factory.protocol.chat = ChatKernel(setup_dict)
    ws_resource = WebSocketResource(factory)

    root = Resource()
    root.putChild(b"", HttpResource())
    root.putChild(b"ws", ws_resource)

    site = Site(root)

    server1.chat.set_outside_request(factory.protocol.chat.from_outside)
    factory.protocol.chat.set_outside_request(server1.chat.from_outside)

    reactor.listenTCP(port2, site)
    reactor.run()
