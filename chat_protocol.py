class ChatProtocol:
    BASE_METHODS = ['login', 'msg', 'msgall', 'logout']
    SPECIAL_METHODS = ['whoami', 'userlist', 'debug']
    AVAILABLE_METHODS = BASE_METHODS + SPECIAL_METHODS

    def __init__(self, **methods):
        self.functions = self.unzip_dict(methods, 0)
        self.args = self.unzip_dict(methods, 1)

    def unzip_dict(self, methods, index):
        funcs = {}
        for key in methods.keys():
            funcs[key] = methods[key][index]
        return funcs

    def merge(self, cmd, **kwargs):
        for key, value in kwargs.items():
            self.args[cmd][key] = value

    def engine(self, cmd, **kwargs):
        self.merge(cmd, **kwargs)
        for method in ChatProtocol.AVAILABLE_METHODS:
            if cmd == method:
                return self.functions[method](**self.args[cmd])


if __name__ == '__main__':
    methods = {'login': ('1', {}),
               'logout': ('2', {}),
               }
    a = ChatProtocol(**methods)
