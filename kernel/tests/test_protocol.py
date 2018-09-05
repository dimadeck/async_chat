import unittest

from kernel.chat_protocol import ChatProtocol


class ProtocolTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.methods = {'login': (cls.get_text, {'suffix': '[SUFFIX]',
                                                'text': ' - login ',
                                                'additional': '(yes)'}),
                       'logout': (cls.get_text, {'suffix': '[SUFFIX]',
                                                 'text': ' - logout ',
                                                 'additional': '(exit)'}),
                       'empty': (cls.get_text, {'suffix': '',
                                                'text': 'empty-method',
                                                'additional': ''})
                       }
        cls.protocol = ChatProtocol(**cls.methods)

    @staticmethod
    def get_text(text=None, suffix=None, additional=None):
        return f'{suffix}{text}{additional}'

    def test_protocol_login(self):
        expected_state = '[SUFFIX] - login (yes)'
        state = self.protocol.engine('login')
        self.assertEqual(expected_state, state)

    def test_protocol_logout(self):
        expected_state = '[SUFFIX] - logout (exit)'
        state = self.protocol.engine('logout')
        self.assertEqual(expected_state, state)

    def test_protocol_empty(self):
        expected_state = 'empty-method'
        state = self.protocol.engine('msgall')
        self.assertEqual(expected_state, state)

    def test_protocol_bad_method(self):
        expected_state = None
        state = self.protocol.engine('Bad')
        self.assertEqual(expected_state, state)


if __name__ == '__main__':
    unittest.main()
