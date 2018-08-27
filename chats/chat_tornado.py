from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer

from chats import VERSION_TOR as VERSION, get_setup_dict
from kernel.chat_kernel import ChatKernel


class EchoServer(TCPServer):
    def __init__(self, connections, port):
        setup_dict = get_setup_dict(connections, VERSION, port)
        self.chat = ChatKernel(setup_dict)
        super(EchoServer, self).__init__()

    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            try:
                data = yield stream.read_until(b"\n")
            except:
                self.chat.logout_engine(stream)
                break
            if self.chat.engine(data, stream, address) == -1:
                break


def main(port=8000, connections=None):
    server = EchoServer(connections=connections, port=port)
    server.listen(port)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.current().close()


if __name__ == "__main__":
    main()
