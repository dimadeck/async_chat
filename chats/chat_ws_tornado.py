import tornado.ioloop
import tornado.web
import tornado.websocket

from chats import TorWsServer
from kernel.chat_kernel import ChatKernel
from kernel.sender import Sender


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html', version=TorWsServer.VERSION)


class WebSocket(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        message = bytes(message, encoding='utf-8')
        request = message.decode('utf-8').strip('')
        self.application.chat.engine(request, self, 'None')

    def on_close(self, message=None):
        self.application.chat.logout_engine(self)


class Application(tornado.web.Application):
    def __init__(self, chat):
        self.chat = chat
        self.chat.add_server(TorWsServer)
        handlers = (
            (r'/', MainHandler),
            (r'/ws', WebSocket))

        tornado.web.Application.__init__(self, handlers)


def main(port=8080):
    chat = ChatKernel(TorWsServer, port, sender=Sender())
    application = Application(chat)
    application.listen(port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except:
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    main()
