from clint.textui import colored

from kernel import *
from kernel.chat_pack_message import PackMessage


class Color:
    @staticmethod
    def change_color(color, message):
        color_set = {'red': colored.red, 'green': colored.green, 'white': colored.white, 'yellow': colored.yellow,
                     'blue': colored.blue, 'black': colored.black}
        if color in color_set:
            return color_set[color](message)
        else:
            return message

    @staticmethod
    def color_suffix(suffix):
        suffix_set = {SERVER_SUFFIX: 'blue', SYSTEM_SUFFIX: 'green', ERROR_SUFFIX: 'red', INFO_SUFFIX: 'blue'}
        if suffix in suffix_set:
            return Color.change_color(suffix_set[suffix], suffix)
        else:
            return suffix

    @staticmethod
    def config_empty_fields(body_parse: list):
        if '' not in body_parse:
            body_parse.insert(1, '')
        if body_parse[0] == '' and body_parse[1] == '':
            body_parse.pop()
        return body_parse

    @staticmethod
    def color_body(body):
        color_set = {'base': 'green', 'add': 'yellow'}
        phrase_set = [MESSAGE_SERVER_START, MESSAGE_NEW_CONNECTION, MESSAGE_LOGIN, MESSAGE_LOGOUT, MESSAGE_FIRST_LOGIN,
                      MESSAGE_ALREADY_LOGIN, MESSAGE_USER_EXIST, MESSAGE_NOT_FOUND]

        final = Color.change_color(color_set['base'], body)

        for phrase in phrase_set:
            if phrase in body:
                final = ''
                body_dict = body.split(phrase)
                body_dict = Color.config_empty_fields(body_dict)
                for chunk in body_dict:
                    if chunk == '':
                        add = Color.change_color(color_set['base'], phrase)
                    else:
                        add = Color.change_color(color_set['add'], chunk)
                    final = f'{final}{add}'
        return final

    @staticmethod
    def color_message(suffix, body):
        color_suffix = Color.color_suffix(suffix)
        color_body = Color.color_body(body)
        return color_suffix, color_body

    @staticmethod
    def color_chat(suffix, body):
        color_suffix = Color.change_color('yellow', suffix)
        color_body = Color.change_color('white', body)
        return color_suffix, color_body

    @staticmethod
    def get_delimeter(phrase):
        if DELIMETER_MESSAGE in phrase:
            return DELIMETER_MESSAGE
        elif DELIMETER_CHAT in phrase:
            return DELIMETER_CHAT
        else:
            return -1

    @staticmethod
    def get_suffix_body(phrase, delimeter):
        parse = phrase.split(delimeter)
        return parse[0], parse[1]

    @staticmethod
    def color_engine(phrase):
        delimeter = Color.get_delimeter(phrase)
        if delimeter == -1:
            return phrase
        else:
            make_color = {DELIMETER_MESSAGE: Color.color_message, DELIMETER_CHAT: Color.color_chat}
            suffix, body = Color.get_suffix_body(phrase, delimeter)
            color_suffix, color_body = make_color[delimeter](suffix, body)

            return f"{color_suffix}{delimeter}{color_body}"


def test():
    phrases = [
        PackMessage.server_message('start', version='test_version', port='test_port'),
        PackMessage.server_message('new', addr='test_addr'),
        PackMessage.server_message('login', username='test_user'),
        PackMessage.server_message('logout', username='test_user'),
        PackMessage.system_message('login', username='test_user'),
        PackMessage.system_message('logout', username='test_user'),
        PackMessage.system_error('bad_request', message='test_error_message'),
        PackMessage.system_error('not_found', username='test_user'), PackMessage.system_error('first_login'),
        PackMessage.system_error('already_login'), PackMessage.system_error('user_exist'),
        PackMessage.chat_message(username='test_user', message='test_message'),
        PackMessage.chat_message(username='test_user', message='test_private_message', private=True),
    ]
    print('#####################[START]#####################')
    for phrase in phrases:
        print(phrase)
    for phrase in phrases:
        print(Color.color_engine(phrase))
    print('#####################[END]#####################')


if __name__ == '__main__':
    test()
