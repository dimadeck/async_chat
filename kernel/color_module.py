from clint.textui import colored

from kernel import DELIMETER_CHAT, DELIMETER_MESSAGE, ERROR_SUFFIX, INFO_SUFFIX, SERVER_SUFFIX, SYSTEM_SUFFIX, \
    MESSAGE_NOT_FOUND, MESSAGE_FIRST_LOGIN, MESSAGE_ALREADY_LOGIN, MESSAGE_LOGIN, MESSAGE_LOGOUT, \
    MESSAGE_NEW_CONNECTION, MESSAGE_SERVER_START, MESSAGE_USER_EXIST


class Color:
    suffix_set = {SERVER_SUFFIX: 'blue', SYSTEM_SUFFIX: 'green', ERROR_SUFFIX: 'red', INFO_SUFFIX: 'blue'}
    suffix_set_html = {SERVER_SUFFIX: 'blue', SYSTEM_SUFFIX: 'SteelBlue', ERROR_SUFFIX: 'Maroon', INFO_SUFFIX: 'blue'}

    body_set = {'base': 'green', 'add': 'yellow'}
    body_set_html = {'base': 'FireBrick', 'add': 'DarkOliveGreen'}

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
        phrase_set = [MESSAGE_SERVER_START, MESSAGE_NEW_CONNECTION, MESSAGE_LOGIN, MESSAGE_LOGOUT, MESSAGE_FIRST_LOGIN,
                      MESSAGE_ALREADY_LOGIN, MESSAGE_USER_EXIST, MESSAGE_NOT_FOUND]
        final = body
        if mode == 'tcp':
            Color.body_set['base'] = 'green'
            final = Color.change_color(Color.body_set['base'], body)
        elif mode == 'ws':
            Color.body_set_html['base'] = 'FireBrick'
            final = Color.change_html_color(Color.body_set_html['base'], body)

        for phrase in phrase_set:
            if phrase in body:
                if phrase == MESSAGE_LOGOUT:
                    Color.body_set['base'] = 'red'
                    Color.body_set_html['base'] = 'DarkRed'
                elif phrase == MESSAGE_LOGIN:
                    Color.body_set['base'] = 'green'
                    Color.body_set_html['base'] = 'DarkGreen'
                else:
                    Color.body_set['base'] = 'green'
                    Color.body_set_html['base'] = 'FireBrick'
                final = ''
                body_dict = body.split(phrase)
                body_dict = Color.config_empty_fields(body_dict)
                for chunk in body_dict:
                    if chunk == '':
                        if mode == 'tcp':
                            add = Color.change_color(Color.body_set['base'], phrase)
                        elif mode == 'ws':
                            add = Color.change_html_color(Color.body_set_html['base'], phrase)
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
    def color_engine(phrase, mode='tcp'):
        delimeter = Color.get_delimeter(phrase)
        if delimeter == -1:
            return phrase
        else:
            make_color = {DELIMETER_MESSAGE: Color.color_message, DELIMETER_CHAT: Color.color_chat}
            suffix, body = Color.get_suffix_body(phrase, delimeter)
            color_suffix, color_body = make_color[delimeter](suffix, body, mode)
            return f"{color_suffix}{delimeter}{color_body}"


def test():
    from kernel.chat_pack_message import PackMessage
    print('#####################[START TCP]#####################')
    phrases = PackMessage(version='testVersion').test()
    for phrase in phrases:
        print(phrase)
    print('#####################[END TCP]#####################')

    print('#####################[START WS]#####################<br>')
    phrases = PackMessage(version='testVersionWS').test()
    for phrase in phrases:
        print(f'{phrase}<br>')
    print('#####################[END WS]#####################')


if __name__ == '__main__':
    test()
