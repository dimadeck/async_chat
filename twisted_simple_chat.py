from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver


class Chat(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.register = False

    def connectionMade(self):
        print("[DEBUG] - New connection")
        self.send_current("What's your name?")

    def connectionLost(self, reason):
        print("[DEBUG] - Lost connection")
        if self.name in self.users:
            self.logging(f'[System] - {self.name} logout.')
            del self.users[self.name]

    def lineReceived(self, line):
        print(f'[DEBUG] - {line}')
        try:
            line = line.decode('utf-8')
        except:
            pass
        if self.register:
            self.chat_engine(line)
        else:
            self.register_engine(line)

    def chat_engine(self, message):
        if message.startswith('/'):
            if message == '/logout':
                self.stopProducing()  # temporary method?
        else:
            message = f'[{self.name}]: {message}'
            self.send_all(message)

    def register_engine(self, name):
        if name in self.users:
            self.send_current("[System] Name taken, please choose another.")
            return
        self.name = name
        self.users[name] = self
        self.register = True
        self.send_current(f"[System] Welcome, {name}!")
        self.logging(f'[System] - {name} login.')

    def send_current(self, msg):
        self.sendLine(bytes(msg, 'utf-8'))

    def send_all(self, message):
        for name, protocol in self.users.items():
            protocol.sendLine(bytes(message, 'utf-8'))

    def logging(self, message):
        print(message)
        self.send_all(message)


class Factory(protocol.ServerFactory):

    def startFactory(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Chat(self.users)


def main(port=1234):
    print(f'[DEBUG] - Twisted Server start on {port}')
    reactor.listenTCP(port, Factory())
    reactor.run()


if __name__ == '__main__':
    main()
