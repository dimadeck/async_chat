from tornado.ioloop import IOLoop
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer


class EchoServer(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            try:
                data = yield stream.read_until(b"\n")
                print(f"Recieved: {data}")
                if not data.endswith(b"\n"):
                    data = data + b"\n"
                yield stream.write(data)
            except StreamClosedError:
                print(f"Log out: {address[0]}")
                break
            except Exception as e:
                print(e)


if __name__ == "__main__":
    server = EchoServer()
    server.listen(8000)
    IOLoop.current().start()
