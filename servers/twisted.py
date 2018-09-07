from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

from kernel.chat_kernel import ChatKernel
from kernel.sender import Sender
from servers import TwServer


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
    def __init__(self, chat):
        self.chat = chat
        super(Factory, self).__init__()

    def buildProtocol(self, addr):
        return Chat(self.chat, addr)


def main(port=8000):
    chat = ChatKernel(TwServer, port, sender=Sender())

    reactor.listenTCP(port, Factory(chat))
    reactor.run()


if __name__ == '__main__':
    main()
