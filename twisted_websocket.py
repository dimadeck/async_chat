from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import listenWS
from twisted.internet import reactor

from kernel.chat_kernel import ChatKernel

VERSION = "Twisted_WS_Chat"


# var ws = new WebSocket("ws://127.0.0.1:9000");
# ws.onmessage = function(e) {alert(e.data);};
# ws.send('message');

class BroadcastServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        print('open')

    def onMessage(self, payload, isBinary):
        print(payload)
        self.sendMessage(payload)

    def connectionLost(self, reason):
        print('lost')
        WebSocketServerProtocol.connectionLost(self, reason)


class BroadcastServerFactory(WebSocketServerFactory):
    def __init__(self, url, connections, port):
        super(BroadcastServerFactory, self).__init__(url)
        self.chat = ChatKernel(connections=connections, parse_strip='', method_send_message=self.send_message,
                               method_close_connection=self.close_connection, version=VERSION, port=port)

    @staticmethod
    def send_message(connection, message):
        mes = {'action': 'response', 'message': message}
        connection.sendMessage(mes)

    @staticmethod
    def close_connection(connection):
        connection.stopProducing()


def main(connections=None, port=1234):
    factory = BroadcastServerFactory('ws://0.0.0.0:9000', connections, port)
    factory.protocol = BroadcastServerProtocol
    listenWS(factory)
    reactor.run()


if __name__ == '__main__':
    main()
