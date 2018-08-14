from clint.textui import colored


class ColorModule:
    @staticmethod
    def color_message(message):
        return ColorModule.change_color('white', message)

    @staticmethod
    def add_suffix(mode, message):
        color_suffix = {
            'error': ColorModule.change_color('red', "[Error]: "),
            'sys': ColorModule.change_color('green', "[System Message]: "),
            'info': ColorModule.change_color('blue', "[INFO]: ")}
        try:
            suffix = color_suffix[mode]
            message = f'{suffix}{message}'
        except:
            pass
        return message

    @staticmethod
    def color_user(username):
        return ColorModule.change_color('yellow', username)

    @staticmethod
    def change_color(color, message):
        color_set = {'red': colored.red, 'green': colored.green, 'white': colored.white, 'yellow': colored.yellow,
                     'blue': colored.blue, 'black': colored.black}
        try:
            return color_set[color](message)
        except:
            return message
