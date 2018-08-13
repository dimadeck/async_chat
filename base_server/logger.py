from clint.textui import colored

SERVER_INFO = True
DEBUG_MODE = False


class Log:
    def __init__(self):
        self.color_set = {'blue': colored.blue, 'yellow': colored.yellow, 'red': colored.red, 'green': colored.green}
        self.kw = None

    def log_engine(self, mode=None, mess=None, **kwargs):
        self.kw = kwargs
        message = None
        color = None
        suffix = None
        if mess is not None:
            print(colored.white(mess))

        if mode is not None:
            if SERVER_INFO:
                suffix = '[SERVER INFO] - '
                message, color = self.server_info(mode)
            if DEBUG_MODE:
                suffix = '[DEBUG] - '
                color = 'blue'
                message = self.debug_mode(mode)

            if message is not None:
                if suffix is not None:
                    message = f'{suffix}{message}'
                if color is not None:
                    message = self.color_set[color](message)

                print(message)

    def server_info(self, mode):
        message = None
        color = None
        if mode == 'login':
            message = f'[{self.kw["username"]}] login to chat.'
            color = 'green'
        elif mode == 'logout':
            message = f'[{self.kw["username"]} logout from chat.'
            color = 'red'
        elif mode == 'new':
            message = f'New connection: {self.kw["addr"]}'
            color = 'yellow'
        return message, color

    def debug_mode(self, mode):
        message = None
        if mode == 'request':
            message = f'Request: {self.kw["data_list"]}'
        elif mode == 'parse':
            message = f'Command: {self.kw["cmd"]}\nParameter: {self.kw["param"]}\nBody: {self.kw["body"]}'
        return message
