from twisted.internet import reactor

from kernel.chat_kernel import ChatKernel
from kernel.sender import Sender
from servers import TwServer, TwWsServer
from servers.twisted import Factory
from servers.twisted_ws import FactoryWS


def main(port1=8000, port2=8080):
    sender = Sender()

    chat1 = ChatKernel(TwServer, port1, sender=sender)
    reactor.listenTCP(port1, Factory(chat1))

    chat2 = ChatKernel(TwWsServer, port2, sender=sender)
    reactor.listenTCP(port2, FactoryWS(chat2, port2).site)
    reactor.run()
