import tornado.ioloop
import tornado.web
import tornado.websocket

from chats import VERSION_TOR_WS as VERSION, get_setup_dict
from kernel.chat_kernel import ChatKernel


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html', version=VERSION)


class WebSocket(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        message = bytes(message, encoding='utf-8')
        request = message.decode('utf-8').strip('')
        self.application.chat.engine(request, self, 'None')

    def on_close(self, message=None):
        self.application.chat.logout_engine(self)


class Application(tornado.web.Application):
    def __init__(self, connections, port):
        setup_dict = get_setup_dict(connections, VERSION, port)
        self.chat = ChatKernel(setup_dict)
        handlers = (
            (r'/', MainHandler),
            (r'/ws', WebSocket))

        tornado.web.Application.__init__(self, handlers)


def main(port=8888, connections=None):
    application = Application(connections, port)
    application.listen(port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except:
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    main()
