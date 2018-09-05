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

    def test_connected_exist_connection_true(self):
        expected_state = True
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        state = self.connections.is_exist_connection('test_connection_1')
        self.assertEqual(expected_state, state)

    def test_connected_exist_connection_false(self):
        expected_state = False
        state = self.connections.is_exist_connection('test_connection_1')
        self.assertEqual(expected_state, state)

    def test_connected_valid_username_ok(self):
        expected_state = 0
        state = self.connections.is_valid_name('Dima')
        self.assertEqual(expected_state, state)

    def test_connected_valid_username_bad_empty(self):
        expected_state = -1
        state = self.connections.is_valid_name('')
        self.assertEqual(expected_state, state)

    def test_connected_valid_username_bad_already_exist(self):
        expected_state = -1
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        state = self.connections.is_valid_name('Dima')
        self.assertEqual(expected_state, state)

    def test_connected_register_ok(self):
        expected_state = 0
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        state = self.connections.register_user('test_connection_1', 'Dima')
        self.assertEqual(expected_state, state)

    def test_connected_register_bad_connection_not_exist(self):
        expected_state = -2
        state = self.connections.register_user('test_connection1', 'Dima')
        self.assertEqual(expected_state, state)

    def test_connected_register_bad(self):
        expected_state = -1
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        state = self.connections.register_user('test_connection_1', 'Dima')
        self.assertEqual(expected_state, state)

    def test_connected_is_register_true(self):
        expected_state = True
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        state = self.connections.is_register('test_connection_1')
        self.assertEqual(expected_state, state)

    def test_connected_is_register_false(self):
        expected_state = False
        state = self.connections.is_register('test_connection1')
        self.assertEqual(expected_state, state)

    def test_connected_get_connection_ok(self):
        expected_state = 'test_connection_1'
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        state = self.connections.get_connection('Dima')
        self.assertEqual(expected_state, state)

    def test_connected_get_connection_bad(self):
        expected_state = None
        state = self.connections.get_connection('Dima')
        self.assertEqual(expected_state, state)

    def test_connected_get_name_ok(self):
        expected_state = 'Dima'
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        state = self.connections.get_name('test_connection_1')
        self.assertEqual(expected_state, state)

    def test_connected_get_name_bad(self):
        expected_state = 0
        state = self.connections.get_name('test_connection_1')
        self.assertEqual(expected_state, state)

    def test_connected_drop_connection_ok_connection(self):
        expected_state = False
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        state = self.connections.is_exist_connection('test_connection_1')
        self.assertEqual(expected_state, state)

    def test_connected_drop_connection_ok_register(self):
        expected_state = False
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        self.connections.drop_connection('test_connection_1')
        state = self.connections.is_register('test_connection_1')
        self.assertEqual(expected_state, state)

    def test_connected_drop_connection_ok_user(self):
        expected_state = {'test_connection_1': 'Dima'}
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        self.connections.add_connection('test_connection_2', 'test_version')
        self.connections.register_user('test_connection_2', 'Alex')
        self.connections.drop_connection('test_connection_2')
        state = self.connections.get_users('test_version')

        self.assertEqual(expected_state, state)

    def test_connected_get_username_list(self):
        expected_state = ['Dima', 'Alex']
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        self.connections.add_connection('test_connection_2', 'test_version')
        self.connections.register_user('test_connection_2', 'Alex')
        state = self.connections.get_username_list()
        self.assertEqual(expected_state, state)

    def test_connected_get_connections(self):
        expected_state = ['test_connection_1', 'test_connection_2']
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        self.connections.add_connection('test_connection_2', 'test_version')
        self.connections.register_user('test_connection_2', 'Alex')
        state = self.connections.get_connections()
        self.assertEqual(expected_state, state)

    def test_connected_get_register_connections(self):
        expected_state = ['test_connection_1']
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        self.connections.add_connection('test_connection_2', 'test_version')
        state = self.connections.get_register_connections()
        self.assertEqual(expected_state, state)

    def test_connected_get_users(self):
        expected_state = {'test_connection_1': 'Dima', 'test_connection_2': 'Alex'}
        self.connections.add_version_header('test_version')
        self.connections.add_connection('test_connection_1', 'test_version')
        self.connections.register_user('test_connection_1', 'Dima')
        self.connections.add_connection('test_connection_2', 'test_version')
        self.connections.register_user('test_connection_2', 'Alex')
        state = self.connections.get_users('test_version')
        self.assertEqual(expected_state, state)


if __name__ == '__main__':
    unittest.main()
