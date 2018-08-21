import tornado.ioloop
import tornado.web
import tornado.websocket

from base_server.connected import Connected
from base_server.tcp_server.tcp_kernel import TCPKernel


# var ws = new WebSocket("ws://127.0.0.1:8888/ws");
# ws.onmessage = function(e) {alert(e.data);};
# ws.send('hello');

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('view/templates/ws_chat.html', version='TORNADO CHAT')


class WebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print('open')
        self.application.chat.add_connection(self)

    def on_message(self, message):
        message = bytes(message, encoding='utf-8')
        self.application.chat.engine(message, self, 'None')
        # if self.application.chat.engine(message, self, 'None') == -1:
        #     self.application.chat.logout(self)

    @staticmethod
    def close_connection(connection):
        connection.close()

    def on_close(self, message=None):
        self.application.chat.logout(self)
        print('close')

    @staticmethod
    def send_message(connection, message):
        mes = {'action': 'response', 'message': message}
        connection.write_message(mes)


class Application(tornado.web.Application):
    def __init__(self):
        self.connections = Connected()
        self.chat = TCPKernel(connections=self.connections, method_send_message=WebSocket.send_message,
                              method_close_connection=WebSocket.close_connection)
        handlers = (
            (r'/', MainHandler),
            (r'/ws', WebSocket))

        tornado.web.Application.__init__(self, handlers)


def main(port=8888):
    application = Application()
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
