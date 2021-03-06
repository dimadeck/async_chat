import tornado

from kernel.chat_kernel import ChatKernel
from kernel.sender import Sender
from servers import TorServer, TorWsServer
from servers.tornado import EchoServer
from servers.tornado_ws import Application


def main(port1=8000, port2=8080):
    sender = Sender()
    chat1 = ChatKernel(TorServer, port1, sender)
    server1 = EchoServer(chat1)
    server1.listen(port1)

    chat2 = ChatKernel(TorWsServer, port2, sender)
    server2 = Application(chat2)
    server2.listen(port2)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except:
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    main()
