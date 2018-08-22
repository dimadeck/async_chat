from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

from kernel.chat_kernel import ChatKernel

VERSION = 'Twisted_Chat'


class Chat(LineReceiver):
    def __init__(self, chat, addr):
        self.chat = chat
        self.addr = addr

    def lineReceived(self, line):
        if self.chat.engine(line, self, self.addr) == -1:
            self.chat.logout_engine(self)

    def connectionLost(self, reason=None):
        self.chat.logout_engine(self)

    @staticmethod
    def send_message(connection, message):
        connection.sendLine(bytes(f'{message}', 'utf-8'))

    @staticmethod
    def close_connection(connection):
        connection.stopProducing()


class Factory(protocol.ServerFactory):
    def __init__(self, connections, port):
        self.chat = ChatKernel(connections=connections, parse_strip='', method_send_message=Chat.send_message,
                               method_close_connection=Chat.close_connection, version=VERSION, port=port)
        self.port = port
        super(Factory, self).__init__()

    def buildProtocol(self, addr):
        return Chat(self.chat, addr)


def main(port=1234, connections=None):
    reactor.listenTCP(port, Factory(connections=connections, port=port))
    reactor.run()


if __name__ == '__main__':
    main()
