class PackMessage:
    SERVER_SUFFIX = '[SERVER INFO]'
    SYSTEM_SUFFIX = '[SYSTEM INFO]'
    ERROR_SUFFIX = '[ERROR]'
    INFO_SUFFIX = '[INFO]'

    MESSAGE_SERVER_START = 'server started on port:'
    MESSAGE_NEW_CONNECTION = 'New connection:'
    MESSAGE_LOGIN = 'login to chat.'
    MESSAGE_LOGOUT = 'logout from chat.'

    MESSAGE_FIRST_LOGIN = 'First login!'
    MESSAGE_ALREADY_LOGIN = 'Already login!'

    MESSAGE_USER_EXIST = 'Username already taken!'
    MESSAGE_NOT_FOUND = 'not found!'

    @staticmethod
    def engine(engine_mode, mode, **kwargs):
        engine_messaging = {
            'server': {'start': (PackMessage.server_start, {kwargs['version'], kwargs['port']}),
                       'new': (PackMessage.server_new_connection, {kwargs['addr']}),
                       'login': (PackMessage.login, {kwargs['username']}),
                       'logout': (PackMessage.logout, {kwargs['username']}),
                       'debug': (PackMessage.message, {kwargs['message']})},
            'system': {'login': (PackMessage.login, {kwargs['username']}),
                       'logout': (PackMessage.logout, {kwargs['username']}),
                       'error': (PackMessage.system_error, {kwargs['error_mode'], kwargs['message']}),
                       'info': (PackMessage.message, {kwargs['message']})
                       },
            'chat': {'message': (PackMessage.chat_message, {kwargs['username'], kwargs['message']})}
        }

        suffix = PackMessage.suffix(engine_mode, mode)
        func = engine_messaging[engine_mode][mode][0]
        args = engine_messaging[engine_mode][mode][1]
        mess = func(args)
        return PackMessage.add_suffix(suffix, mess)

    @staticmethod
    def system_error(error_mode, **kwargs):
        error_messaging = {'bad_request': kwargs['message'],
                           'first_login': PackMessage.MESSAGE_FIRST_LOGIN,
                           'already_login': PackMessage.MESSAGE_ALREADY_LOGIN,
                           'user_exist': PackMessage.MESSAGE_USER_EXIST,
                           'not_found': PackMessage.MESSAGE_NOT_FOUND}
        return error_messaging[error_mode]

    @staticmethod
    def suffix(m1, m2):
        if m1 == 'chat':
            suffix = None
        elif m1 == 'server':
            suffix = PackMessage.SERVER_SUFFIX
        else:
            if m2 == ('login' or 'logout'):
                suffix = PackMessage.SYSTEM_SUFFIX
            elif m2 == 'error':
                suffix = PackMessage.ERROR_SUFFIX
            else:
                suffix = PackMessage.INFO_SUFFIX
        return suffix

    @staticmethod
    def add_suffix(suffix, message):
        mess = f'{suffix} - {message}'
        return mess

    @staticmethod
    def server_start(version, port):
        mess = f'{version} {PackMessage.MESSAGE_SERVER_START} {port}'
        return mess

    @staticmethod
    def server_new_connection(addr):
        mess = f'{PackMessage.MESSAGE_NEW_CONNECTION} {addr}.'
        return mess

    @staticmethod
    def login(username):
        mess = f'[{username}] {PackMessage.MESSAGE_LOGIN}'
        return mess

    @staticmethod
    def logout(username):
        mess = f'[{username}] {PackMessage.MESSAGE_LOGOUT}'
        return mess

    @staticmethod
    def chat_message(username, message, private=False):
        private_sym = '*' if private else ''
        mess = f'[{username}{private_sym}]: {message}'
        return mess

    @staticmethod
    def message(message):
        return message
