import time

from kernel import *


# from kernel.color_module import Color


class PackMessage:
    def __init__(self, version):
        self.version = version
        self.color = True
        if self.version is not None:
            self.color_mode = 'ws' if 'WS' in self.version else 'tcp'

    def server_message(self, server_mode, port=None, addr=None, username=None, message=None):
        if server_mode == 'start':
            message = self.server_start(self.version, port)
        elif server_mode == 'new':
            message = self.server_new_connection(addr)
        elif server_mode == 'login':
            message = self.login(username)
        elif server_mode == 'logout':
            message = self.logout(username)
        mess = self.add_suffix(SERVER_SUFFIX, message)
        # mess = Color.color_engine(mess)
        mess = f'[{self.version}] - {mess}'
        return mess

    def system_message(self, system_mode, username=None, message=None):
        if system_mode == 'login':
            message = self.login(username)
        elif system_mode == 'logout':
            message = self.logout(username)
        mess = self.add_suffix(SYSTEM_SUFFIX, message)
        # mess = Color.color_engine(mess, self.color_mode)
        return mess

    def chat_message(self, username, message, private=False, target=None):
        private_sym = '[->]' if private else ''
        target = f'[{target}]' if target is not None else ''
        mess = f'[{time.strftime("%H:%M:%S")}][{username}]{private_sym}{target}{DELIMETER_CHAT}{message}'
        # mess = Color.color_engine(mess, self.color_mode)
        return mess

    def system_info(self, message=None, clear_data=False):
        if clear_data:
            return message
        mess = self.add_suffix(INFO_SUFFIX, message)
        # mess = Color.color_engine(mess, self.color_mode)
        return mess

    def system_error(self, error_mode, message=None, username=None):
        error_messaging = {'bad_request': message,
                           'first_login': MESSAGE_FIRST_LOGIN,
                           'already_login': MESSAGE_ALREADY_LOGIN,
                           'user_exist': MESSAGE_USER_EXIST,
                           'not_found': f'[{username}] {MESSAGE_NOT_FOUND}'}

        mess = self.add_suffix(ERROR_SUFFIX, error_messaging[error_mode])
        # mess = Color.color_engine(mess, self.color_mode)
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

    def test(self):
        phrases = [
            self.server_message('start', port='test_port'),
            self.server_message('new', addr='test_addr'),
            self.server_message('login', username='test_user'),
            self.server_message('logout', username='test_user'),
            self.system_message('login', username='test_user'),
            self.system_message('logout', username='test_user'),
            self.system_error('bad_request', message='test_error_message'),
            self.system_error('not_found', username='test_user'), self.system_error('first_login'),
            self.system_error('already_login'), self.system_error('user_exist'),
            self.chat_message(username='test_user', message='test_message'),
            self.chat_message(username='test_user', message='test_private_message', private=True),
        ]
        return phrases
