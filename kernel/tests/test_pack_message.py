import time
import unittest

from kernel.chat_pack_message import PackMessage
from kernel.color_module import Color


class PackMessageTest(unittest.TestCase):
    def test_pack_message_prepare_login(self):
        expected_message = '[SYSTEM INFO] - [Dima] login to chat.'
        message = PackMessage().prepare_message('login', username='Dima')
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_logout(self):
        expected_message = '[SYSTEM INFO] - [Dima] logout from chat.'
        message = PackMessage().prepare_message('logout', username='Dima')
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_send_message(self):
        timer = time.strftime("%H:%M:%S")
        expected_message = f'[{timer}][Dima][->][Alex]: Hello, my friend!'
        message = PackMessage().prepare_message('send_message', sender='Dima',
                                                message='Hello, my friend!', username='Alex')
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_send_all(self):
        timer = time.strftime("%H:%M:%S")
        expected_message = f'[{timer}][Dima]: Hello, guys!'
        message = PackMessage().prepare_message('send_message_all', username='Dima', message='Hello, guys!')
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_info_whoami(self):
        expected_message = '[INFO] - Dima'
        message = PackMessage().prepare_message('info', info_mode='whoami', username='Dima')
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_info_whoami_clear(self):
        expected_message = 'Dima'
        message = PackMessage().prepare_message('info', info_mode='whoami', username='Dima', clear_data=True)
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_info_userlist(self):
        userlist = ['Dima', 'Alex', 'Mark']
        expected_message = f"[INFO] - ['Dima', 'Alex', 'Mark']"
        message = PackMessage().prepare_message('info', info_mode='userlist', userlist=userlist)
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_info_userlist_clear(self):
        userlist = str(['Dima', 'Alex', 'Mark'])
        expected_message = f"['Dima', 'Alex', 'Mark']"
        message = PackMessage().prepare_message('info', info_mode='userlist', userlist=userlist, clear_data=True)
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_error_bad_request(self):
        expected_message = '[ERROR] - Bad Request'
        message = PackMessage().prepare_message('error', error_mode='bad_request', message='Bad Request')
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_error_first_login(self):
        expected_message = '[ERROR] - First login!'
        message = PackMessage().prepare_message('error', error_mode='first_login')
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_error_already_login(self):
        expected_message = '[ERROR] - Already login!'
        message = PackMessage().prepare_message('error', error_mode='already_login')
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_error_user_exist(self):
        expected_message = '[ERROR] - Username already taken!'
        message = PackMessage().prepare_message('error', error_mode='user_exist')
        self.assertEqual(expected_message, message)

    def test_pack_message_prepare_error_not_found(self):
        expected_message = '[ERROR] - [Dima] not found!'
        message = PackMessage().prepare_message('error', error_mode='not_found', username='Dima')
        self.assertEqual(expected_message, message)

    def test_pack_message_server_message_start(self):
        mess = Color.color_engine('[SERVER INFO] - test_version server started on port: test_port')
        expected_message = f'[test_version] - {mess}'

        message = PackMessage().server_message('start', version='test_version', port='test_port')
        self.assertEqual(expected_message, message)

    def test_pack_message_server_message_new(self):
        mess = Color.color_engine('[SERVER INFO] - New connection: test_addr.')
        expected_message = f'[test_version] - {mess}'

        message = PackMessage().server_message('new', version='test_version', addr='test_addr')
        self.assertEqual(expected_message, message)

    def test_pack_message_server_message_login(self):
        mess = Color.color_engine('[SERVER INFO] - [Dima] login to chat.')
        expected_message = f'[test_version] - {mess}'

        message = PackMessage().server_message('login', version='test_version', username='Dima')
        self.assertEqual(expected_message, message)

    def test_pack_message_server_message_logout(self):
        mess = Color.color_engine('[SERVER INFO] - [Dima] logout from chat.')
        expected_message = f'[test_version] - {mess}'
        message = PackMessage().server_message('logout', version='test_version', username='Dima')
        self.assertEqual(expected_message, message)


if __name__ == '__main__':
    unittest.main()
