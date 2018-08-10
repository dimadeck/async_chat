from tornado.ioloop import IOLoop
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

from asyncio_simple_chat.connected import Connected


class EchoServer(TCPServer):
    def __init__(self):
        super().__init__()
        self.connected = Connected()

    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            try:
                data = yield stream.read_until(b"\n")
                data = data.decode("utf-8").strip("\r\n")
                print(f'Recieved: {data}')
                yield stream.write(bytes(data, 'utf-8'))
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
