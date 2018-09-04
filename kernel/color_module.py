from clint.textui import colored

from kernel import DELIMETER_CHAT, DELIMETER_MESSAGE, ERROR_SUFFIX, INFO_SUFFIX, SERVER_SUFFIX, SYSTEM_SUFFIX, \
    MESSAGE_NOT_FOUND, MESSAGE_FIRST_LOGIN, MESSAGE_ALREADY_LOGIN, MESSAGE_LOGIN, MESSAGE_LOGOUT, \
    MESSAGE_NEW_CONNECTION, MESSAGE_SERVER_START, MESSAGE_USER_EXIST


class Color:
    phrase_set = [MESSAGE_SERVER_START, MESSAGE_NEW_CONNECTION, MESSAGE_LOGIN, MESSAGE_LOGOUT, MESSAGE_FIRST_LOGIN,
                  MESSAGE_ALREADY_LOGIN, MESSAGE_USER_EXIST, MESSAGE_NOT_FOUND]

    suffix_set = {SERVER_SUFFIX: 'blue', SYSTEM_SUFFIX: 'green', ERROR_SUFFIX: 'red', INFO_SUFFIX: 'blue'}
    suffix_set_html = {SYSTEM_SUFFIX: 'SteelBlue', ERROR_SUFFIX: 'Maroon', INFO_SUFFIX: 'blue'}

    body_set = {'base': 'green', 'add': 'yellow', 'login': 'green', 'logout': 'red'}
    body_set_html = {'base': 'FireBrick', 'add': 'DarkOliveGreen', 'login': 'DarkGreen', 'logout': 'DarkRed'}

    chat_set = {'base': 'white', 'add': 'yellow'}
    chat_set_html = {'base': 'Black', 'add': 'DarkSlateBlue'}

    @staticmethod
    def change_color(color, message):
        color_set = {'red': colored.red, 'green': colored.green, 'white': colored.white, 'yellow': colored.yellow,
                     'blue': colored.blue, 'black': colored.black}
        if color in color_set:
            return color_set[color](message)
        else:
            return message

    @staticmethod
    def change_html_color(color, message):
        return f'<font color="{color}">{message}</font>'

    @staticmethod
    def color_suffix(suffix, mode):
        if suffix in Color.suffix_set and mode == 'tcp':
            return Color.change_color(Color.suffix_set[suffix], suffix)
        elif suffix in Color.suffix_set_html and mode == 'ws':
            return Color.change_html_color(Color.suffix_set_html[suffix], suffix)
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
    def color_body(body, mode):
        if mode == 'ws':
            final = Color.change_html_color(Color.body_set_html['base'], body)
        else:
            final = Color.change_color(Color.body_set['base'], body)

        for phrase in Color.phrase_set:
            if phrase in body:
                if phrase == MESSAGE_LOGOUT:
                    current_col = Color.body_set['logout']
                    current_col_html = Color.body_set_html['logout']
                elif phrase == MESSAGE_LOGIN:
                    current_col = Color.body_set['login']
                    current_col_html = Color.body_set_html['login']
                else:
                    current_col = Color.body_set['base']
                    current_col_html = Color.body_set_html['base']
                final = ''
                body_dict = body.split(phrase)
                body_dict = Color.config_empty_fields(body_dict)
                for chunk in body_dict:
                    if chunk == '':
                        if mode == 'tcp':
                            add = Color.change_color(current_col, phrase)
                        elif mode == 'ws':
                            add = Color.change_html_color(current_col_html, phrase)
                    else:
                        if mode == 'tcp':
                            add = Color.change_color(Color.body_set['add'], chunk)
                        elif mode == 'ws':
                            add = Color.change_html_color(Color.body_set_html['add'], chunk)
                    final = f'{final}{add}'
        return final

    @staticmethod
    def color_message(suffix, body, mode):
        suffix = Color.color_suffix(suffix, mode)
        body = Color.color_body(body, mode)
        return suffix, body

    @staticmethod
    def color_chat(suffix, body, mode):
        if mode == 'tcp':
            suffix = Color.change_color(Color.chat_set['add'], suffix)
            body = Color.change_color(Color.chat_set['base'], body)
        elif mode == 'ws':
            suffix = Color.change_html_color(Color.chat_set_html['add'], suffix)
            body = Color.change_html_color(Color.chat_set_html['base'], body)
        return suffix, body

    @staticmethod
    def get_delimiter(phrase):
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
    def color_engine(phrase, mode='tcp'):
        delimiter = Color.get_delimiter(phrase)
        if delimiter == -1:
            return phrase
        else:
            make_color = {DELIMETER_MESSAGE: Color.color_message, DELIMETER_CHAT: Color.color_chat}
            suffix, body = Color.get_suffix_body(phrase, delimiter)
            color_suffix, color_body = make_color[delimiter](suffix, body, mode)
            return f"{color_suffix}{delimiter}{color_body}"
