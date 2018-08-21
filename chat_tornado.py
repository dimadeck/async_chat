from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer
from kernel.chat_kernel import ChatKernel
from kernel.chat_pack_message import PackMessage


class EchoServer(TCPServer, ChatKernel):
    def __init__(self, connections):
        ChatKernel.__init__(self, connections, parse_strip='\r\n', method_send_message=self.send_message,
                            method_close_connection=self.close_connection)
        super(EchoServer, self).__init__()

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


VERSION = "Tornado_Chat"


def main(port=8000, connections=None):
    server = EchoServer(connections=connections)
    server.listen(port)
    print(PackMessage.server_message('start', version=VERSION, port=port))
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.current().close()


if __name__ == "__main__":
    main()
