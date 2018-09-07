from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer

from kernel.chat_kernel import ChatKernel
from kernel.sender import Sender
from servers import TorServer


class EchoServer(TCPServer):
    def __init__(self, chat):
        self.chat = chat
        super(EchoServer, self).__init__()

    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            try:
                data = yield stream.read_until(b"\n")
            except:
                self.chat.logout_engine(stream)
                break
            request = data.decode('utf-8').strip('\r\n')
            if self.chat.engine(request, stream, address) == -1:
                break


def main(port=8000):
    chat = ChatKernel(TorServer, port, sender=Sender())
    server = EchoServer(chat)
    server.listen(port)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.current().stop()


if __name__ == "__main__":
    main()
