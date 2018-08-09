from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver


class MyChatProtocol(LineReceiver):
    def connectionMade(self):
        print("New connection")
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Lost connection")
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        print(line)
        for c in self.factory.clients:
            if c is not self:
                c.sendLine(line)

    def send_message(self, msg):
        pass


class MyChatFactory(protocol.ServerFactory):
    protocol = MyChatProtocol

    def startFactory(self):
        self.clients = []


if __name__ == '__main__':
    reactor.listenTCP(1234, MyChatFactory())
    reactor.run()
