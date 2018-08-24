from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import listenWS
from twisted.internet import reactor

from kernel.chat_kernel import ChatKernel

VERSION = "Twisted_WS_Chat"


class TwistedWsProtocol(WebSocketServerProtocol):
    def onOpen(self):
        print('open')

    def onMessage(self, payload, isBinary):
        print(payload)
        self.chat.engine(payload, self, 'None')

    def connectionLost(self, reason):
        print('lost')
        self.chat.logout_engine(self)


def main(connections=None, port=1234):
    factory = WebSocketServerFactory(f'ws://127.0.0.1:{port}')
    factory.protocol = TwistedWsProtocol
    factory.protocol.chat = ChatKernel(connections=connections, parse_strip='', method_send_message=send_message,
                                       method_close_connection=close_connection, version=VERSION, port=port)
    listenWS(factory)
    reactor.run()


def send_message(connection, message):
    # mes = {'action': 'response', 'message': message}
    connection.sendMessage(bytes(message, encoding='utf-8'))


def close_connection(connection):
    pass


if __name__ == '__main__':
    # var ws = new WebSocket("ws://127.0.0.1:1234");
    # ws.onmessage = function(e) {console.info(e.data);};
    # ws.send('message');
    main()
