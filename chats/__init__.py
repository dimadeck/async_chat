import json

from kernel.color_module import Color


class AsServer:
    VERSION = 'AsyncIO_Chat'

    @staticmethod
    async def send_message(connection, message):
        message = add_color(message, 'tcp')
        await connection.write(bytes(f'{message}\n', 'utf-8'))

    @staticmethod
    async def close_connection(connection):
        connection.close()


class AsWsServer:
    VERSION = 'AsyncIO_WS_Chat'

    @staticmethod
    async def send_message(connection, message):
        mes = prepare_ws_message(message)
        await connection.send_json(mes)

    @staticmethod
    async def close_connection(connection):
        await connection.close()


class TwServer:
    VERSION = 'Twisted_Chat'

    @staticmethod
    def send_message(connection, message):
        message = add_color(message, 'tcp')
        connection.sendLine(bytes(f'{message}', 'utf-8'))

    @staticmethod
    def close_connection(connection):
        connection.stopProducing()


class TwWsServer:
    VERSION = 'Twisted_WS_Chat'

    @staticmethod
    def close_connection(connection):
        connection.sendClose()

    @staticmethod
    def send_message(connection, message):
        mes = json.dumps(prepare_ws_message(message))
        connection.sendMessage(bytes(mes, encoding='utf-8'))


class TorServer:
    VERSION = 'Tornado_Chat'

    @staticmethod
    def send_message(connect, message):
        message = add_color(message, 'tcp')
        connect.write(bytes(f'{message}\n', 'utf-8'))

    @staticmethod
    def close_connection(connection):
        connection.close()


class TorWsServer:
    VERSION = 'Tornado_WS_Chat'

    @staticmethod
    def send_message(connection, message):
        mes = prepare_ws_message(message)
        connection.write_message(mes)

    @staticmethod
    def close_connection(connection):
        connection.close()


def add_color(message, mode):
    mess = Color.color_engine(message, mode)
    return mess


def prepare_ws_message(message):
    if type(message) == list:
        mes = {'action': 'list', 'message': message}
    else:
        mes = {'action': 'response', 'message': add_color(message, 'ws')}
    return mes
