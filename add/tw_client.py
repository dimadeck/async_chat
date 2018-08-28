from twisted.internet import protocol, reactor


class Twist_client(protocol.Protocol):
    def sendData(self):
        data = input()
        if data:
            self.transport.write(bytes(data, 'utf-8'))
        else:
            self.transport.loseConnection()

    def connectionMade(self):
        self.sendData()

    def dataReceived(self, data):
        print(data)
        self.sendData()


class Twist_Factory(protocol.ClientFactory):
    protocol = Twist_client

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        reactor.stop()


def main():
    factory = Twist_Factory()
    reactor.connectTCP('127.0.0.1', 10000, factory)
    reactor.run()


if __name__ == '__main__':
    main()
