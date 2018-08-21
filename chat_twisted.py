from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

from kernel.chat_kernel import ChatKernel
from kernel.chat_pack_message import PackMessage


class Chat(LineReceiver, ChatKernel):
    def __init__(self, connections, addr):
        super(Chat, self).__init__(connections=connections, parse_strip='', method_send_message=self.send_message,
                                   method_close_connection=self.close_connection)
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
        self.connections = ChatKernel.init_connection_list(connections)
        super(Factory, self).__init__()

    def buildProtocol(self, addr):
        return Chat(self.connections, addr)


VERSION = 'Twisted_Chat'


def main(port=1234, connections=None):
    print(PackMessage.server_message('start', version=VERSION, port=port))
    reactor.listenTCP(port, Factory(connections=connections))
    reactor.run()


if __name__ == '__main__':
    main()
