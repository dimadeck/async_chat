import unittest

from kernel.connected import Connected


class ConnectedTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.connections = Connected()

    def test_connected_add_version_ok(self):
        expected_state = 0
        state = self.connections.add_version_header('test_version')
        self.assertEqual(expected_state, state)

    def test_connected_add_version_bad(self):
        expected_state = -1
        self.connections.add_version_header('test_version')
        state = self.connections.add_version_header('test_version')
        self.assertEqual(expected_state, state)

    def test_connected_add_connection_ok(self):
        expected_state = 0
        self.connections.add_version_header('test_version')
        state = self.connections.add_connection('test_connection_1', 'test_version')
        self.assertEqual(expected_state, state)

    def test_connected_add_connection_bad_already_in_list(self):
        expected_state = -1
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        state = self.connections.add_connection('test_connection_1', 'test_version')
        self.assertEqual(expected_state, state)

    def test_connected_add_connection_bad_version(self):
        expected_state = -2
        self.connections.add_version_header('test_version')
        state = self.connections.add_connection('test_connection_1', 'test1_version')
        self.assertEqual(expected_state, state)

    def test_connected_get_connections_by_version(self):
        expected_state = ['test_connection_1', 'test_connection_2']
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.add_connection('test_connection_2', 'test_version')
        state = self.connections.get_connections_by_version('test_version')
        self.assertEqual(expected_state, state)

    def test_connected_get_version_by_connections_ok(self):
        expected_state = 'test_version1'
        self.connections.add_version_header('test_version')
        self.connections.add_version_header('test_version1')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.add_connection('test_connection_2', 'test_version1')
        state = self.connections.get_version_by_connection('test_connection_2')
        self.assertEqual(expected_state, state)

    def test_connected_get_version_by_connections_bad_connection_not_exist(self):
        expected_state = -2
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        state = self.connections.get_version_by_connection('test_connection_2')
        self.assertEqual(expected_state, state)

    def test_connected_get_version_by_connections_bad_version_not_registered(self):
        expected_state = -1
        self.connections.add_connection('test_connection_1', 'test_version')
        state = self.connections.get_version_by_connection('test_connection_1')
        self.assertEqual(expected_state, state)


if __name__ == '__main__':
    unittest.main()
