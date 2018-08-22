import tornado.ioloop
import tornado.web
import tornado.websocket

from kernel.chat_kernel import ChatKernel
from kernel.chat_pack_message import PackMessage


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


class Application(tornado.web.Application):
    def __init__(self, connections):
        self.chat = ChatKernel(connections=connections, method_send_message=WebSocket.send_message, parse_strip='',
                               method_close_connection=WebSocket.close_connection)
        handlers = (
            (r'/', MainHandler),
            (r'/ws', WebSocket))

        tornado.web.Application.__init__(self, handlers)


VERSION = 'TORNADO_WS_CHAT'


def main(port=8888, connections=None):
    application = Application(connections)
    application.listen(port)
    print(PackMessage.server_message('start', version=VERSION, port=port))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
