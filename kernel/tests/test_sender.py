import unittest

from kernel.sender import Sender


class TestServer:
    VERSION = 'TEST_SERVER_VERSION'
    TEST_STATE = None

    @staticmethod
    def send_message(connection, message):
        TestServer.TEST_STATE = f'for: {connection}. test_send_message: {message}'

    @staticmethod
    def close_connection(connection):
        TestServer.TEST_STATE = f'test_close_connection: {connection}'


class SenderTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.sender = Sender()
        cls.sender.add_server(TestServer)
        cls.sender.add_version(TestServer.VERSION)
        cls.sender.add_connection('test_connection_1', TestServer.VERSION)
        cls.sender.login('test_connection_1', 'Dima')

    def test_sender_servers_server(self):
        expected_server = [TestServer]
        server = list(self.sender.servers.values())
        self.assertEqual(expected_server, server)

    def test_sender_servers_version(self):
        expected_server = ['TEST_SERVER_VERSION']
        server = list(self.sender.servers.keys())
        self.assertEqual(expected_server, server)

    def test_sender_send_all(self):
        TestServer.TEST_STATE = ''
        expected_value = 'for: test_connection_1. test_send_message: hello'
        self.sender.send_all('hello')
        self.assertEqual(expected_value, TestServer.TEST_STATE)

    def test_sender_close_connection(self):
        TestServer.TEST_STATE = ''
        expected_value = 'test_close_connection: test_connection_1'
        self.sender.close('test_connection_1')
        self.assertEqual(expected_value, TestServer.TEST_STATE)

    def test_sender_logout_close(self):
        expected_value = 'test_close_connection: test_connection_1'
        self.sender.logout('test_connection_1')
        self.assertEqual(expected_value, TestServer.TEST_STATE)

    def test_sender_logout_drop(self):
        expected_value = ['test_connection_2']
        self.sender.add_connection('test_connection_2', TestServer.VERSION)
        self.sender.login('test_connection_2', 'Alex')
        self.sender.logout('test_connection_1')
        value = self.sender.get_connections()
        self.assertEqual(expected_value, value)


if __name__ == '__main__':
    unittest.main()
