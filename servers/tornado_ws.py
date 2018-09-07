import tornado.ioloop
import tornado.web
import tornado.websocket

from kernel.chat_kernel import ChatKernel
from kernel.sender import Sender
from servers import TorWsServer


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
        handlers = (
            (r'/ws', WebSocket),
            (r'/(.*)', tornado.web.StaticFileHandler, {"path": "chats/templates/", 'default_filename': "index.html"}))

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
