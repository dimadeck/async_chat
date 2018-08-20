import json
from collections import namedtuple

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import listenWS
from twisted.internet import reactor


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.username = None
        self.factory.register(self)
        self.factory.broadcastChatUsers()
        self.sendChat()

    def onMessage(self, payload, isBinary):
        print(payload)
        if not isBinary:
            message = payload.decode('utf8')
            if message.startswith('/username'):
                self.setUsername(message.split(' ', 1)[-1])
                print('Client username set to "{}"'.format(self))
            else:
                self.factory.broadcast(self, message)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)
        self.factory.broadcastChatUsers()

    def sendEntry(self, entry):
        message = json.dumps({
            'sender': str(entry.sender),
            'message': entry.message
        })
        self.sendMessage(message)
        print('Message "{}" sent to {}'.format(message, self))

    def sendChat(self):
        for entry in self.factory.chat:
            self.sendEntry(entry)

    def sendChatUsers(self):
        message = '/users {}'.format(','.join([str(user) for user in self.factory.users]))
        self.sendMessage(message)

    def setUsername(self, username):
        self.username = username
        print('Client username set to "{}"'.format(self))
        self.factory.broadcastChatUsers()

    def __str__(self):
        return self.username or self.peer


Entry = namedtuple('Entry', ['sender', 'message'])


class BroadcastServerFactory(WebSocketServerFactory):
    def __init__(self, url):
        super(BroadcastServerFactory, self).__init__(url)
        self.users = []
        self.chat = []

    def register(self, user):
        if user not in self.users:
            print("Registered user {}".format(user))
            self.users.append(user)

    def unregister(self, user):
        if user in self.users:
            print("Unregistered user {}".format(user))
            self.users.remove(user)

    def broadcast(self, sender, message):
        print("Broadcasting message '{}' from {}".format(
            message.encode('utf8'), sender
        ))
        entry = Entry(sender=sender, message=message)
        for user in self.users:
            user.sendEntry(entry)
        self.chat.append(entry)

    def broadcastChatUsers(self):
        for user in self.users:
            user.sendChatUsers()


if __name__ == '__main__':
    factory = BroadcastServerFactory('ws://0.0.0.0:9000')
    factory.protocol = BroadcastServerProtocol
    listenWS(factory)
    reactor.run()
