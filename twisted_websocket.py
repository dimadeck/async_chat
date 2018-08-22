from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import listenWS
from twisted.internet import reactor
VERSION = "TWISTED"

class BroadcastServerProtocol(WebSocketServerProtocol):
    def get(self):
        self.render('view/templates/ws_chat.html', version=VERSION)

    def onOpen(self):
        print('open')

    def onMessage(self, payload, isBinary):
        print(payload)
        self.sendMessage(payload)

    def connectionLost(self, reason):
        print('lost')
        WebSocketServerProtocol.connectionLost(self, reason)


class BroadcastServerFactory(WebSocketServerFactory):
    def __init__(self, url):
        super(BroadcastServerFactory, self).__init__(url)
        self.users = []


if __name__ == '__main__':
    factory = BroadcastServerFactory('ws://0.0.0.0:9000')
    factory.protocol = BroadcastServerProtocol
    listenWS(factory)
    reactor.run()
