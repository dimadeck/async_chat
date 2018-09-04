import time

from kernel import *

from kernel.color_module import Color


class PackMessage:
    @staticmethod
    def prepare_message(mode, username=None, message=None, error_mode=None, info_mode=None, clear_data=None,
                        sender=None, userlist=None, version=None):
        if mode == ('login' or 'logout'):
            print(PackMessage.server_message(mode, username=username, version=version))
            message = PackMessage.system_message(mode, username=username)
        elif mode == 'send_message':
            message = PackMessage.chat_message(username=sender, message=message, private=True, target=username)
        elif mode == 'send_message_all':
            message = PackMessage.chat_message(username=username, message=message)
        elif mode == 'info':
            info_set = {'whoami': username, 'userlist': userlist}
            message = PackMessage.system_info(info_set[info_mode], clear_data)
        elif mode == 'error':
            message = PackMessage.system_error(error_mode, message=message, username=username)
        return message

    @staticmethod
    def server_message(server_mode, port=None, addr=None, username=None, message=None, version=None):
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
        mess = f'[{version}] - {mess}'
        return mess

    @staticmethod
    def system_message(system_mode, username=None, message=None):
        if system_mode == 'login':
            message = PackMessage.login(username)
        elif system_mode == 'logout':
            message = PackMessage.logout(username)
        mess = PackMessage.add_suffix(SYSTEM_SUFFIX, message)
        return mess

    @staticmethod
    def chat_message(username, message, private=False, target=None):
        private_sym = '[->]' if private else ''
        target = f'[{target}]' if target is not None else ''
        mess = f'[{time.strftime("%H:%M:%S")}][{username}]{private_sym}{target}{DELIMETER_CHAT}{message}'
        return mess

    @staticmethod
    def system_info(message=None, clear_data=False):
        if clear_data:
            return message
        mess = PackMessage.add_suffix(INFO_SUFFIX, message)
        return mess

    @staticmethod
    def system_error(error_mode, message=None, username=None):
        error_messaging = {'bad_request': message,
                           'first_login': MESSAGE_FIRST_LOGIN,
                           'already_login': MESSAGE_ALREADY_LOGIN,
                           'user_exist': MESSAGE_USER_EXIST,
                           'not_found': f'[{username}] {MESSAGE_NOT_FOUND}'}

        mess = PackMessage.add_suffix(ERROR_SUFFIX, error_messaging[error_mode])
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
