from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

from base_server.tcp_server.tcp_kernel import TCPKernel


class Chat(LineReceiver, TCPKernel):
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
    def __init__(self, connections):
        super(Factory, self).__init__()
        self.connections = TCPKernel.init_connection_list(connections)

    def buildProtocol(self, addr):
        return Chat(self.connections, addr)


def main(port=1234, connections=None):
    print(f'[SERVER INFO] - Twisted server started on {port} port.')
    reactor.listenTCP(port, Factory(connections=connections))
    reactor.run()


if __name__ == '__main__':
    main()
