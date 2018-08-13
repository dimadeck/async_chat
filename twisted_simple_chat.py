from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
from base_server.base_server import ChatKernel
from base_server.connected import Connected
from base_server.data_parser import DataParser


class Chat(LineReceiver, ChatKernel):
    def __init__(self, users):
        super(Chat, self).__init__(connections=users)

    def connectionMade(self):
        print("[DEBUG] - New connection")

    def connectionLost(self, reason):
        print("[DEBUG] - Lost connection")

    def lineReceived(self, line):
        print(f'[DEBUG] - {line}')
        req_dict = DataParser(line, strip='')
        writer = self
        self.engine(line, writer, 'fake address', req_dict)

    @staticmethod
    def send_message(connection, message):
        connection.sendLine(bytes(f'{message}', 'utf-8'))


class Factory(protocol.ServerFactory):
    def startFactory(self):
        self.users = Connected()

    def buildProtocol(self, addr):
        return Chat(self.users)


def main(port=1234):
    print(f'[DEBUG] - Twisted Server start on {port}')
    reactor.listenTCP(port, Factory())
    reactor.run()


if __name__ == '__main__':
    main()
