import sys

from twisted.internet import protocol, reactor


class MessageServer:
    def __init__(self, port):
        self.factory = protocol.Factory()
        self.factory.protocol = MessageServer.MessageServerProtocol
        print(f'Connected server start on port: {port}')
        reactor.listenTCP(port, self.factory)
        reactor.run()

    class MessageServerProtocol(protocol.Protocol):
        def dataReceived(self, request):
            print(request)
            if len(request) > 0:
                self.transport.write(bytes(f'{request}', 'utf-8'))


class MessageClient:
    def __init__(self, port):
        self.factory = protocol.ClientFactory()
        self.factory.protocol = MessageClient.MessageClientProtocol
        reactor.connectTCP('127.0.0.1', port, self.factory)
        reactor.run()

    class MessageClientProtocol(protocol.Protocol):
        def dataReceived(self, data):
            print(data)


def main(port=10000):
    server = MessageServer(port)


def main_client(port=10000):
    client = MessageClient(port)


if __name__ == '__main__':
    if sys.argv[1] == 'client':
        main_client()
    else:
        main()
