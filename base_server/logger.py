from clint.textui import colored

SERVER_INFO = True
DEBUG_MODE = False


class Log:
    def __init__(self):
        self.color_set = {'blue': colored.blue, 'yellow': colored.yellow, 'red': colored.red, 'green': colored.green}

    def log_engine(self, mode=None, mess=None, **kwargs):
        message = None
        color = None
        suffix = None
        if mess is not None:
            print(colored.white(mess))

        if mode is not None:
            if SERVER_INFO:
                suffix = '[SERVER INFO] - '
                message, color = self.server_info(mode, kwargs=kwargs)
            if DEBUG_MODE:
                suffix = '[DEBUG] - '
                color = 'blue'
                message = self.debug_mode(mode, kwargs=kwargs)

            if message is not None:
                if suffix is not None:
                    message = f'{suffix}{message}'
                if color is not None:
                    message = self.color_set[color](message)

                print(message)

    @staticmethod
    def server_info(mode, **kwargs):
        message = None
        color = None
        if mode == 'login':
            message = f'[{kwargs["username"]}] login to chat.'
            color = 'green'
        elif mode == 'logout':
            message = f'[{kwargs["username"]} logout from chat.'
            color = 'red'
        elif mode == 'new':
            message = f'New connection: {kwargs["addr"]}'
            color = 'yellow'
        return message, color

    @staticmethod
    def debug_mode(mode, **kwargs):
        message = None
        if mode == 'request':
            message = f'Request: {kwargs["data_list"]}'
        elif mode == 'parse':
            message = f'Command: {kwargs["cmd"]}\nParameter: {kwargs["param"]}\nBody: {kwargs["body"]}'
        return message
