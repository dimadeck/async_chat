from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from clint.textui import colored

port = 8000


class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = "REGISTER"

    def connectionMade(self):
        print("New connection")
        self.sendLine(bytes("You're connected", 'utf-8'))
        self.sendLine(bytes("Choose a username:", 'utf-8'))

    def connectionLost(self, reason):
        leftMsg = f'{self.name} has left the channel.'
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.broadcastMessage(leftMsg)

    def lineReceived(self, line):
        if self.state == "REGISTER":
            self.handle_REGISTER(line)
        else:
            self.handle_CHAT(line)

    def handle_REGISTER(self, name):
        if name in self.factory.users:
            self.sendLine(bytes(f'Sorry, {name} is taken. Try something else.', 'utf-8'))
            return

        joinedMsg = colored.green('%s has joined the chanel.' % (name,))
        self.broadcastMessage(joinedMsg)
        self.name = name
        self.factory.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = self.getTime() + "<%s> %s" % (self.name, message)
        self.broadcastMessage(colored.magenta(message))

    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.items():
            print(f'name = {name}')
            print(f'protocol = {protocol}')
            if protocol != self:
                protocol.sendLine(bytes(colored.white(message), 'utf-8'))


class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)


reactor.listenTCP(port, ChatFactory())
print("Chat Server started on port %s" % (port,))
reactor.run()
