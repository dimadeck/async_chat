import tornado

from chats.chat_tornado import EchoServer
from chats.chat_ws_tornado import Application


def main(port1=8000, port2=8080, connections=None):
    server1 = EchoServer(connections=connections, port=port1)
    server1.listen(port1)

    server2 = Application(server1.chat.connections, port2)
    server2.listen(port2)

    server1.chat.set_outside_request(server2.chat.from_outside)
    server2.chat.set_outside_request(server1.chat.from_outside)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except:
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    main()
