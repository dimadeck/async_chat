from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from twisted.internet import reactor

# var ws = new WebSocket("ws://127.0.0.1:9000");
# ws.onmessage = function(e) {alert(e.data);};
# ws.send('hello');
from base_server.tcp_server.tcp_kernel import TCPKernel
from kernel.chat_kernel import ChatKernel


class MyServerProtocol(WebSocketServerProtocol, ChatKernel):

    def onConnect(self, request):
        print(f"Client connecting: {request.peer}")
        self.sendMessage(bytes('Connect', encoding='utf-8'))

    def onClose(self, wasClean, code, reason):
        print(f"WebSocket connection closed: {reason}")

    def onMessage(self, payload, isBinary):
        print(f"Message: {payload.decode('utf8')}")
        self.sendMessage(payload, isBinary)


if __name__ == '__main__':
    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol()
    reactor.listenTCP(9000, factory)
    reactor.run()
