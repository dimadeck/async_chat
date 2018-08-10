from tornado.ioloop import IOLoop
from tornado import gen
from tornado.tcpserver import TCPServer
from base_server.base_server import ChatKernel
from base_server.connected import Connected


class EchoServer(TCPServer, ChatKernel):
    def __init__(self):
        super(EchoServer, self).__init__()
        self.connected = Connected()

    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            data = yield stream.read_until(b"\n")
            if self.engine(data, stream, address) == -1:
                break


def main():
    server = EchoServer()
    server.listen(8000)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.current().close()


if __name__ == "__main__":
    main()
