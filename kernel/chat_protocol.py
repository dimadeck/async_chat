from kernel import AVAILABLE_METHODS


class ChatProtocol:

    def __init__(self, **methods):
        self.functions = self.unzip_dict(methods, 0)
        self.args = self.unzip_dict(methods, 1)
        self.empty_method = self.get_empty_function(**methods)

        self.fill_empty(self.empty_method)

    @staticmethod
    def unzip_dict(methods, index):
        funcs = {}
        for key in methods.keys():
            funcs[key] = methods[key][index]
        return funcs

    def fill_empty(self, func):
        for method in AVAILABLE_METHODS:
            if method not in self.functions.keys():
                self.functions[method] = func[0]
                self.args[method] = func[1]

    def get_empty_function(self, **methods):
        try:
            return methods['empty']
        except KeyError:
            return self.empty_function, {}

    def empty_function(self):
        pass

    def engine(self, cmd):
        for method in AVAILABLE_METHODS:
            if cmd == method:
                return self.functions[cmd](**self.args[cmd])
