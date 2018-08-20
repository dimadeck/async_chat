class ChatProtocol:
    BASE_METHODS = ['login', 'msg', 'msgall', 'logout']
    SPECIAL_METHODS = ['whoami', 'userlist', 'debug']
    AVAILABLE_METHODS = BASE_METHODS + SPECIAL_METHODS
