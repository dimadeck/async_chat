import tornado.ioloop
import tornado.web
import tornado.websocket

from base_server.connected import Connected
from base_server.tcp_server.data_parser import DataParser


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('view/templates/ws_chat.html', version='1')


class WebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print('open')
        self.application.connections.add_connection(self)

    def on_message(self, message):
        message = bytes(message, encoding='utf-8')
        req_dict = DataParser(message, strip='')
        print(req_dict.data_list)
        mes = None
        # if req_dict[0] == 'login':
        #     self.application.connections.register_user(self, message_dict[1])
        #     mes = {'action': 'connect', 'name': }
        #     self.write_message(mes)
        #     mes = {'action': 'join', 'name': message_dict[1]}
        # if mes is not None:
        #     for ws in self.application.connections.users:
        #         ws.write_message(mes)

    def on_close(self, message=None):
        self.application.connections.drop_connection(self)


class PackMessage:
    def __init__(self, mode='ws'):
        self.mode = mode

    def new_connection(self, name):
        if self.mode == 'ws':
            mess = {'action': 'connect', 'name': name}


class Application(tornado.web.Application):
    def __init__(self):
        self.connections = Connected()
        self.pack_message = PackMessage(mode='ws')

        handlers = (
            (r'/', MainHandler),
            (r'/ws', WebSocket))

        tornado.web.Application.__init__(self, handlers, connections=self.connections)


def main(port=8888):
    application = Application()
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
