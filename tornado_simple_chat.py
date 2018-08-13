from tornado.ioloop import IOLoop
from tornado import gen
from tornado.tcpserver import TCPServer
from base_server.base_server import ChatKernel
from base_server.connected import Connected
from base_server.data_parser import DataParser


class EchoServer(TCPServer, ChatKernel):
    def __init__(self):
        super(EchoServer, self).__init__()
        self.connected = Connected()

    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            data = yield stream.read_until(b"\n")
            parse_list = DataParser(data)
            if self.engine(data, stream, address, parse_list) == -1:
                break

    @staticmethod
    def send_message(connection, message):
        connection.write(bytes(f'{message}\n', 'utf-8'))


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
