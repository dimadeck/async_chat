from tornado.ioloop import IOLoop
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer
from base_server.base_server import ChatKernel


class EchoServer(TCPServer, ChatKernel):
    def __init__(self):
        super(EchoServer, self).__init__()
        super(ChatKernel, self).__init__()

    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            try:
                data = yield stream.read_until(b"\n")
                if self.engine(data, stream) == -1:
                    break
                # yield stream.write(bytes(data, 'utf-8'))
            except StreamClosedError:
                print(f"Log out: {address}")
                break
            except Exception as e:
                print(e)


def main():
    server = EchoServer()
    server.listen(8000)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.current().close()


if __name__ == "__main__":
    main()
