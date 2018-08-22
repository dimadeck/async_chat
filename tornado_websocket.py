import tornado.ioloop
import tornado.web
import tornado.websocket

from kernel.chat_kernel import ChatKernel

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('view/templates/ws_chat.html', version=VERSION)


class WebSocket(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        message = bytes(message, encoding='utf-8')
        self.application.chat.engine(message, self, 'None')

    @staticmethod
    def close_connection(connection):
        connection.close()

    def on_close(self, message=None):
        self.application.chat.logout_engine(self)
        print('close')

    @staticmethod
    def send_message(connection, message):
        mes = {'action': 'response', 'message': message}
        connection.write_message(mes)


VERSION = 'TORNADO_WS_CHAT'


class Application(tornado.web.Application):
    def __init__(self, connections, port):
        self.chat = ChatKernel(connections=connections, method_send_message=WebSocket.send_message, parse_strip='',
                               method_close_connection=WebSocket.close_connection, version=VERSION, port=port)
        handlers = (
            (r'/', MainHandler),
            (r'/ws', WebSocket))

        tornado.web.Application.__init__(self, handlers)


def main(port=8888, connections=None):
    application = Application(connections, port)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
