import json

import tornado.web
import tornado.ioloop
import tornado.websocket


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('view/templates/index.html', version='1')


class WebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        self.render('view/templates/index.html', version='1')
        self.application.webSocketsPool.append(self)

    def on_message(self, message):
        db = self.application.db
        message_dict = json.loads(message)
        db.chat.insert(message_dict)
        for key, value in enumerate(self.application.webSocketsPool):
            if value != self:
                value.ws_connection.write_message(message)

    def on_close(self, message=None):
        for key, value in enumerate(self.application.webSocketsPool):
            if value == self:
                del self.application.webSocketsPool[key]


class Application(tornado.web.Application):
    def __init__(self):
        self.webSocketsPool = []

        handlers = (
            (r'/', MainHandler),
            (r'/websocket/?', WebSocket))

        tornado.web.Application.__init__(self, handlers)

application = Application()


if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()