from base_server.color_module import ColorChat, ColorServer, Color


class PackMessage:
    @staticmethod
    def text_message(is_exist, private=True, sender=None, username=None, body=None):
        private_sym = '*' if private else ''
        if is_exist:
            message = ' '.join(body)
            sender = ColorChat.color_user(sender)
            message = ColorChat.color_message(message)
            message = f'[{sender}{private_sym}]: {message}'
        else:
            message = 'not found!'
            username = ColorChat.color_user(username)
            message = ColorChat.add_suffix('error', f'[{username}]: {message}')
        return message

    @staticmethod
    def send_success_login(username):
        ColorServer.log_engine(mode='login', username=username)
        message = "login to chat."
        message = Color.change_color('green', message)

        username = ColorChat.color_user(username)
        message = f'[{username}] {message}'
        message = ColorChat.add_suffix('sys', message)
        return message

    @staticmethod
    def send_already_login(username):
        username = ColorChat.color_user(username)
        message = 'already exist!'
        message = f'[{username}]: {message}'
        message = ColorChat.add_suffix('error', message)
        return message

    @staticmethod
    def send_response_for_bad_request(req_dict):
        message = req_dict.STATUS_DICT[req_dict.status]
        message = ColorChat.add_suffix('error', message)
        return message

    @staticmethod
    def send_logout(username):
        ColorServer.log_engine(mode='logout', username=username)

        message = "logout from chat."
        message = Color.change_color('red', message)
        username = ColorChat.color_user(username)
        message = f'[{username}] {message}'
        message = ColorChat.add_suffix('sys', message)
        return message

    @staticmethod
    def send_first_login():
        message = 'First login!'
        message = ColorChat.add_suffix('error', message)
        return message

    @staticmethod
    def get_info(cmd, message=None):
        if cmd == 'whoami':
            message = ColorChat.add_suffix('info', message)
        elif cmd == 'userlist':
            message = ColorChat.add_suffix('info', message)
        elif cmd == 'login':
            message = 'Already login!'
            message = ColorChat.add_suffix('error', message)
        return message
