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
    def server_message(server_mode, version=None, port=None, addr=None, username=None, message=None):
        if server_mode == 'start':
            message = PackMessage.server_start(version, port)
        elif server_mode == 'new':
            message = PackMessage.server_new_connection(addr)
        elif server_mode == 'login':
            message = PackMessage.login(username)
        elif server_mode == 'logout':
            message = PackMessage.logout(username)

        return PackMessage.add_suffix(PackMessage.SERVER_SUFFIX, message)

    @staticmethod
    def system_message(system_mode, username=None, message=None):
        if system_mode == 'login':
            message = PackMessage.login(username)
        elif system_mode == 'logout':
            message = PackMessage.logout(username)

        return PackMessage.add_suffix(PackMessage.SYSTEM_SUFFIX, message)

    @staticmethod
    def chat_message(username, message, private=False):
        private_sym = '*' if private else ''
        mess = f'[{username}{private_sym}]: {message}'
        return mess

    @staticmethod
    def system_error(error_mode, message=None, username=None):
        error_messaging = {'bad_request': message,
                           'first_login': PackMessage.MESSAGE_FIRST_LOGIN,
                           'already_login': PackMessage.MESSAGE_ALREADY_LOGIN,
                           'user_exist': PackMessage.MESSAGE_USER_EXIST,
                           'not_found': f'[{username}] {PackMessage.MESSAGE_NOT_FOUND}'}
        return PackMessage.add_suffix(PackMessage.ERROR_SUFFIX, error_messaging[error_mode])

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
    def message(message):
        return message
