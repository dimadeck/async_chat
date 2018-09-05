import unittest

from kernel.chat_kernel import ChatKernel
from kernel.chat_pack_message import PackMessage
from kernel.sender import Sender


class TestServer:
    VERSION = 'TEST_CHAT_SERVER_VERSION'
    TEST_MESSAGE_STATE = None
    TEST_CLOSE_STATE = None

    @staticmethod
    def send_message(connection, message):
        TestServer.TEST_MESSAGE_STATE = f'{connection}: {message}'

    @staticmethod
    def close_connection(connection):
        TestServer.TEST_CLOSE_STATE = f'Close connection: {connection}'


class KernelTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        TestServer.TEST_CLOSE_STATE = None
        TestServer.TEST_MESSAGE_STATE = None
        cls.chat = ChatKernel(TestServer, 'test_port', Sender())
        cls.chat.engine('login Dima', 'test_connection_1', '-')

    def test_kernel_login_answer(self):
        mess = PackMessage.prepare_message('login', username='Dima')
        expected_line = f"test_connection_1: {mess}"
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_login_connections(self):
        expected_line = ['test_connection_1']
        line = self.chat.sender.get_connections()
        self.assertEqual(expected_line, line)

    def test_kernel_login_username_list(self):
        expected_line = ['Dima']
        line = self.chat.sender.get_username_list()
        self.assertEqual(expected_line, line)

    def test_kernel_login_users(self):
        expected_line = {'test_connection_1': 'Dima'}
        line = self.chat.sender.get_users(self.chat.version)
        self.assertEqual(expected_line, line)

    def test_kernel_logout_answer(self):
        mess = PackMessage.prepare_message('logout', username='Dima2')
        expected_line = f"test_connection_2: {mess}"

        self.chat.engine('login Dima2', 'test_connection_2', '-')
        self.chat.engine('logout', 'test_connection_2', '-')
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_logout_close_answer(self):
        expected_line = 'Close connection: test_connection_2'
        self.chat.engine('login Dima2', 'test_connection_2', '-')
        self.chat.engine('logout', 'test_connection_2', '-')
        line = TestServer.TEST_CLOSE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_logout_connections(self):
        expected_line = ['test_connection_1']
        self.chat.engine('login Dima2', 'test_connection_2', '-')
        self.chat.engine('logout', 'test_connection_2', '-')
        line = self.chat.sender.get_connections()
        self.assertEqual(expected_line, line)

    def test_kernel_logout_username_list(self):
        expected_line = ['Dima']
        self.chat.engine('login Dima2', 'test_connection_2', '-')
        self.chat.engine('logout', 'test_connection_2', '-')
        line = self.chat.sender.get_username_list()
        self.assertEqual(expected_line, line)

    def test_kernel_logout_users(self):
        expected_line = {'test_connection_1': 'Dima'}
        self.chat.engine('login Dima2', 'test_connection_2', '-')
        self.chat.engine('logout', 'test_connection_2', '-')
        line = self.chat.sender.get_users(self.chat.version)
        self.assertEqual(expected_line, line)

    def test_kernel_login_already(self):
        mess = PackMessage.prepare_message('error', error_mode='already_login', username='Dima')
        expected_line = f"test_connection_1: {mess}"
        self.chat.engine('login Dima', 'test_connection_1', '-')
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_send_message_ok(self):
        mess = PackMessage.prepare_message('send_message', sender='Dima', message='hello!', username='Dima')
        expected_line = f"test_connection_1: {mess}"
        self.chat.engine('msg Dima hello!', 'test_connection_1', '-')
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_send_message_not_exist_user(self):
        mess = PackMessage.prepare_message('error', error_mode='not_found', username='NoBody')
        expected_line = f"test_connection_1: {mess}"
        self.chat.engine('msg NoBody hello!', 'test_connection_1', '-')
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_send_message_all(self):
        mess = PackMessage.prepare_message('send_message_all', message='Hello!', username='Dima')
        expected_line = f"test_connection_1: {mess}"
        self.chat.engine('msgall Hello!', 'test_connection_1', '-')
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_whoami(self):
        mess = PackMessage.prepare_message('info', info_mode='whoami', username='Dima')
        expected_line = f'test_connection_1: {mess}'
        self.chat.engine('whoami', 'test_connection_1', '-')
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_whoami_clear_data(self):
        expected_line = 'test_connection_1: Dima'
        self.chat.engine('/whoami', 'test_connection_1', '-')
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_userlist(self):
        mess = PackMessage.prepare_message('info', info_mode='userlist', userlist="['Dima']")
        expected_line = f'test_connection_1: {mess}'
        self.chat.engine('userlist', 'test_connection_1', '-')
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_userlist_clear_data(self):
        expected_line = "test_connection_1: ['Dima']"
        self.chat.engine('/userlist', 'test_connection_1', '-')
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_first_login(self):
        mess = PackMessage.prepare_message('error', error_mode='first_login')
        expected_line = f"test_connection_1: {mess}"
        self.chat.engine('', 'test_connection_1', '-')
        self.chat.engine('msgall hello!', 'test_connection_1', '-')
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)

    def test_kernel_bad_request(self):
        mess = PackMessage.prepare_message('error', error_mode='bad_request', message='empty message')
        expected_line = f"test_connection_1: {mess}"
        self.chat.engine('', 'test_connection_1', '-')
        self.chat.engine('msgall', 'test_connection_1', '-')
        line = TestServer.TEST_MESSAGE_STATE
        self.assertEqual(expected_line, line)


if __name__ == '__main__':
    unittest.main()
