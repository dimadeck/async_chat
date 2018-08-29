from twisted.internet import protocol, reactor


class Twist(protocol.Protocol):
    def dataReceived(self, data):
        print(data)
        self.transport.write(data)

def main():
    factory = protocol.Factory()
    factory.protocol = Twist
    reactor.listenTCP(10000, factory)
    reactor.run()


if __name__ == '__main__':
    main()