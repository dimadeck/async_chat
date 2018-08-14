from clint.textui import colored

SERVER_INFO = True
DEBUG_MODE = False


class Color:
    @staticmethod
    def change_color(color, message):
        color_set = {'red': colored.red, 'green': colored.green, 'white': colored.white, 'yellow': colored.yellow,
                     'blue': colored.blue, 'black': colored.black}
        try:
            return color_set[color](message)
        except:
            return message


class ColorChat:
    @staticmethod
    def color_message(message):
        return Color.change_color('white', message)

    @staticmethod
    def add_suffix(mode, message):
        color_suffix = {
            'error': Color.change_color('red', "[Error]: "),
            'sys': Color.change_color('green', "[System Message]: "),
            'info': Color.change_color('blue', "[INFO]: ")}
        try:
            suffix = color_suffix[mode]
            message = f'{suffix}{message}'
        except:
            pass
        return message

    @staticmethod
    def color_user(username):
        return Color.change_color('yellow', username)


class ColorServer:
    @staticmethod
    def log_engine(mode=None, mess=None, **kw):
        message = None
        color = None
        suffix = None
        if mess is not None:
            print(Color.change_color('white', mess))

        if mode is not None:
            if SERVER_INFO:
                suffix = '[SERVER INFO] - '
                message, color = ColorServer.server_info(mode, **kw)
            if DEBUG_MODE:
                suffix = '[DEBUG] - '
                color = 'blue'
                message = ColorServer.debug_mode(mode, **kw)

            if message is not None:
                if suffix is not None:
                    message = f'{suffix}{message}'
                if color is not None:
                    message = Color.change_color(color, message)

                print(message)

    @staticmethod
    def server_info(mode, **kw):
        message = None
        color = None
        if mode == 'login':
            message = f'[{kw["username"]}] login to chat.'
            color = 'green'
        elif mode == 'logout':
            message = f'[{kw["username"]}] logout from chat.'
            color = 'red'
        elif mode == 'new':
            message = f'New connection: {kw["addr"]}'
            color = 'yellow'
        return message, color

    @staticmethod
    def debug_mode(mode, **kw):
        message = None
        if mode == 'request':
            message = f'Request: {kw["data_list"]}'
        elif mode == 'parse':
            message = f'Command: {kw["cmd"]}\nParameter: {kw["param"]}\nBody: {kw["body"]}'
        return message
