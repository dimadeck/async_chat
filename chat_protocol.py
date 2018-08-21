class ChatProtocol:
    BASE_METHODS = ['login', 'msg', 'msgall', 'logout']
    SPECIAL_METHODS = ['whoami', 'userlist', 'debug']
    AVAILABLE_METHODS = BASE_METHODS + SPECIAL_METHODS

    def __init__(self, **methods):
        self.functions = self.unzip_dict(methods, 0)
        self.args = self.unzip_dict(methods, 1)
        try:
            self.empty_method = methods['empty']
        except KeyError:
            self.empty_method = (self.empty_function, {})
        self.fill_empty(self.empty_method)

    @staticmethod
    def unzip_dict(methods, index):
        funcs = {}
        for key in methods.keys():
            funcs[key] = methods[key][index]
        return funcs

    # def merge(self, cmd, **kwargs):
    #     for key, value in kwargs.items():
    #         self.args[cmd][key] = value

    def fill_empty(self, func):
        print(func)
        print(func[0])
        for method in ChatProtocol.AVAILABLE_METHODS:
            if method not in self.functions.keys():
                self.functions[method] = func[0]
                self.args[method] = func[1]
        print('')
        print(self.functions)
        print('')

    def engine(self, cmd):
        for method in ChatProtocol.AVAILABLE_METHODS:
            if cmd == method:
                return self.functions[cmd](**self.args[cmd])

    def empty_function(self):
        pass


if __name__ == '__main__':
    methods = {'login': ('1', {}),
               'logout': ('2', {}),
               }
    a = ChatProtocol(**methods)
