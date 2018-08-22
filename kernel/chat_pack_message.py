from kernel import *
from kernel.color_module import Color


class PackMessage:
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
        mess = PackMessage.add_suffix(SERVER_SUFFIX, message)
        mess = Color.color_engine(mess)
        return mess

    @staticmethod
    def system_message(system_mode, username=None, message=None):
        if system_mode == 'login':
            message = PackMessage.login(username)
        elif system_mode == 'logout':
            message = PackMessage.logout(username)
        mess = PackMessage.add_suffix(SYSTEM_SUFFIX, message)
        mess = Color.color_engine(mess)
        return mess

    @staticmethod
    def chat_message(username, message, private=False):
        private_sym = '*' if private else ''
        mess = f'[{username}][{private_sym}]{DELIMETER_CHAT}{message}'
        mess = Color.color_engine(mess)
        return mess

    @staticmethod
    def system_error(error_mode, message=None, username=None):
        error_messaging = {'bad_request': message,
                           'first_login': MESSAGE_FIRST_LOGIN,
                           'already_login': MESSAGE_ALREADY_LOGIN,
                           'user_exist': MESSAGE_USER_EXIST,
                           'not_found': f'[{username}] {MESSAGE_NOT_FOUND}'}

        mess = PackMessage.add_suffix(ERROR_SUFFIX, error_messaging[error_mode])
        mess = Color.color_engine(mess)
        return mess

    @staticmethod
    def add_suffix(suffix, message):
        mess = f'{suffix}{DELIMETER_MESSAGE}{message}'
        return mess

    @staticmethod
    def server_start(version, port):
        mess = f'{version} {MESSAGE_SERVER_START} {port}'
        return mess

    @staticmethod
    def server_new_connection(addr):
        mess = f'{MESSAGE_NEW_CONNECTION} {addr}.'
        return mess

    @staticmethod
    def login(username):
        mess = f'[{username}] {MESSAGE_LOGIN}'
        return mess

    @staticmethod
    def logout(username):
        mess = f'[{username}] {MESSAGE_LOGOUT}'
        return mess

    @staticmethod
    def message(message):
        return message

    @staticmethod
    def test():
        phrases = [
            PackMessage.server_message('start', version='test_version', port='test_port'),
            PackMessage.server_message('new', addr='test_addr'),
            PackMessage.server_message('login', username='test_user'),
            PackMessage.server_message('logout', username='test_user'),
            PackMessage.system_message('login', username='test_user'),
            PackMessage.system_message('logout', username='test_user'),
            PackMessage.system_error('bad_request', message='test_error_message'),
            PackMessage.system_error('not_found', username='test_user'), PackMessage.system_error('first_login'),
            PackMessage.system_error('already_login'), PackMessage.system_error('user_exist'),
            PackMessage.chat_message(username='test_user', message='test_message'),
            PackMessage.chat_message(username='test_user', message='test_private_message', private=True),
        ]
        return phrases
