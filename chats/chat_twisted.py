from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

from chats import VERSION_TW as VERSION, get_setup_dict
from kernel.chat_kernel import ChatKernel


class Chat(LineReceiver):
    def __init__(self, chat, addr):
        self.chat = chat
        self.addr = addr

    def lineReceived(self, line):
        request = line.decode('utf-8').strip('')
        if self.chat.engine(request, self, self.addr) == -1:
            self.chat.logout_engine(self)

    def connectionLost(self, reason=None):
        self.chat.logout_engine(self)


class Factory(protocol.ServerFactory):
    def __init__(self, connections, port):
        setup_dict = get_setup_dict(connections, VERSION, port)
        self.chat = ChatKernel(setup_dict)
        super(Factory, self).__init__()

    def buildProtocol(self, addr):
        return Chat(self.chat, addr)


def main(port=1234, connections=None):
    reactor.listenTCP(port, Factory(connections=connections, port=port))
    reactor.run()


if __name__ == '__main__':
    main()
