from tornado.ioloop import IOLoop
from tornado import gen
from tornado.tcpserver import TCPServer
from base_server.base_server import ChatKernel
from base_server.connected import Connected


class EchoServer(TCPServer, ChatKernel):
    def __init__(self):
        super(EchoServer, self).__init__()
        self.connections = Connected()
        self.parse_strip = '\r\n'

    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            data = yield stream.read_until(b"\n")
            if self.engine(data, stream, address) == -1:
                break

    @staticmethod
    def send_message(connection, message):
        connection.write(bytes(f'{message}\n', 'utf-8'))

    @staticmethod
    def close_connection(connection):
        connection.close()


def main():
    server = EchoServer()
    port = 8000
    server.listen(port)
    print(f'[SERVER INFO] - Tornado server started on {port} port.')

    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.current().close()


if __name__ == "__main__":
    main()
