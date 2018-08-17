from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer

from base_server.tcp_server.tcp_kernel import TCPKernel


class EchoServer(TCPServer, TCPKernel):
    def __init__(self, connections):
        super(EchoServer, self).__init__()
        self.connections = self.init_connection_list(connections)
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


def main(port=8000, connections=None):
    server = EchoServer(connections=connections)
    server.listen(port)
    print(f'[SERVER INFO] - Tornado server started on {port} port.')

    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.current().close()


if __name__ == "__main__":
    main()
