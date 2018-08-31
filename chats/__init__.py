import json

VERSION_AS = 'AsyncIO_Chat'
VERSION_TW = 'Twisted_Chat'
VERSION_TOR = 'Tornado_Chat'
VERSION_AS_WS = 'AsyncIO_WS_Chat'
VERSION_TW_WS = 'Twisted_WS_Chat'
VERSION_TOR_WS = 'Tornado_WS_Chat'


async def as_send_message(connection, message):
    await connection.write(bytes(f'{message}\n', 'utf-8'))


def tw_send_message(connection, message):
    connection.sendLine(bytes(f'{message}', 'utf-8'))


async def as_ws_close_connection(connection):
    await connection.close()


async def as_ws_send_message(connection, message):
    mes = prepare_ws_message(message)
    await connection.send_json(mes)


def tor_send_message(connect, message):
    connect.write(bytes(f'{message}\n', 'utf-8'))


def tor_ws_send_message(connection, message):
    mes = prepare_ws_message(message)
    connection.write_message(mes)


def tw_ws_send_message(connection, message):
    mes = json.dumps(prepare_ws_message(message))
    connection.sendMessage(bytes(mes, encoding='utf-8'))


def prepare_ws_message(message):
    if type(message) == list:
        mes = {'action': 'list', 'message': message}
    else:
        mes = {'action': 'response', 'message': message}
    return mes


async def as_close_connection(connection):
    connection.close()


def tor_close_connection(connection):
    connection.close()


def tw_close_connection(connection):
    connection.stopProducing()


def tor_ws_close_connection(connection):
    connection.close()


def tw_ws_close_connection(connection):
    connection.sendClose()


send_mess_dict = {VERSION_AS: as_send_message, VERSION_TOR: tor_send_message, VERSION_TW: tw_send_message,
                  VERSION_AS_WS: as_ws_send_message, VERSION_TOR_WS: tor_ws_send_message,
                  VERSION_TW_WS: tw_ws_send_message}
close_connection_dict = {VERSION_AS: as_close_connection, VERSION_TOR: tor_close_connection,
                         VERSION_TW: tw_close_connection,
                         VERSION_AS_WS: as_ws_close_connection, VERSION_TOR_WS: tor_ws_close_connection,
                         VERSION_TW_WS: tw_ws_close_connection}


def get_setup_dict(connections, version, port):
    setup_dict = {'connections': connections, 'version': version, 'port': port, 'parse_strip': ''}
    if version == VERSION_AS or version == VERSION_TOR:
        setup_dict['parse_strip'] = '\r\n'
    setup_dict['method_send_message'] = send_mess_dict[version]
    setup_dict['method_close_connection'] = close_connection_dict[version]

    return setup_dict


def test():
    print(get_setup_dict('AS', VERSION_AS, 1000))
    print(get_setup_dict('TOR', VERSION_TOR, 2000))
    print(get_setup_dict('TW', VERSION_TW, 3000))
    print(get_setup_dict('AS_WS', VERSION_AS_WS, 4000))
    print(get_setup_dict('TOR_WS', VERSION_TOR_WS, 5000))
    print(get_setup_dict('TW_WS', VERSION_TW_WS, 6000))


if __name__ == '__main__':
    test()
