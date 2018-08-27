VERSION_AS = 'AsyncIO_Chat'
VERSION_TW = 'Twisted_Chat'
VERSION_TOR = 'Tornado_Chat'
VERSION_AS_WS = 'AsyncIO_WS_Chat'
VERSION_TW_WS = 'Twisted_WS_Chat'
VERSION_TOR_WS = 'Tornado_WS_Chat'


async def as_send_message(connection, message):
    connection.write(bytes(f'{message}\n', 'utf-8'))


def tor_send_message(connection, message):
    connection.write(bytes(f'{message}\n', 'utf-8'))


def tw_send_message(connection, message):
    connection.sendLine(bytes(f'{message}', 'utf-8'))


async def as_ws_close_connection(connection):
    await connection.close()


def tor_ws_send_message(connection, message):
    mes = {'action': 'response', 'message': message}
    connection.write_message(mes)


def tw_ws_send_message(connection, message):
    connection.sendMessage(bytes(message, 'utf-8'))


async def as_close_connection(connection):
    connection.close()


def tor_close_connection(connection):
    connection.close()


def tw_close_connection(connection):
    connection.stopProducing()


async def as_ws_send_message(connection, message):
    mes = {'action': 'response', 'message': message}
    await connection.send_json(mes)


def tor_ws_close_connection(connection):
    connection.close()


def tw_ws_close_connection(connection):
    connection.sendClose()


def get_setup_dict(connections, version, port):
    setup_dict = {'connections': connections, 'version': version, 'port': port, 'parse_strip': ''}

    if version == VERSION_AS or version == VERSION_TOR:
        setup_dict['parse_strip'] = '\r\n'

    as_dict = {'method_send_message': as_send_message,
               'method_close_connection': as_close_connection}

    tor_dict = {'method_send_message': tor_send_message,
                'method_close_connection': tor_close_connection}

    tw_dict = {'method_send_message': tw_send_message,
               'method_close_connection': tw_close_connection}

    as_ws_dict = {'method_send_message': as_ws_send_message,
                  'method_close_connection': as_ws_close_connection}

    tor_ws_dict = {'method_send_message': tor_ws_send_message,
                   'method_close_connection': tor_ws_close_connection}

    tw_ws_dict = {'method_send_message': tw_ws_send_message,
                  'method_close_connection': tw_ws_close_connection}
    update_dict = {VERSION_AS: as_dict, VERSION_TOR: tor_dict, VERSION_TW: tw_dict,
                   VERSION_AS_WS: as_ws_dict, VERSION_TOR_WS: tor_ws_dict, VERSION_TW_WS: tw_ws_dict}
    setup_dict.update(update_dict[version])
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
