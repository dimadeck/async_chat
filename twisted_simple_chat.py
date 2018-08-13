from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

from base_server.base_server import ChatKernel
from base_server.connected import Connected


class Chat(LineReceiver, ChatKernel):
    def __init__(self, connections, addr):
        super(Chat, self).__init__(connections=connections, parse_strip='')
        self.addr = addr

    def lineReceived(self, line):
        self.engine(line, self, self.addr)

    @staticmethod
    def send_message(connection, message):
        connection.sendLine(bytes(f'{message}', 'utf-8'))

    @staticmethod
    def close_connection(connection):
        connection.stopProducing()


class Factory(protocol.ServerFactory):
    def startFactory(self):
        self.connections = Connected()

    def buildProtocol(self, addr):
        return Chat(self.connections, addr)


def main(port=1234):
    print(f'[DEBUG] - Twisted Server start on {port}')
    reactor.listenTCP(port, Factory())
    reactor.run()


if __name__ == '__main__':
    main()
