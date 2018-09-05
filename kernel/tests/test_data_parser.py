import unittest

from kernel.data_parser import DataParser


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expected_line1 = 1

    def test_parser_template(self):
        line2 = 1
        self.assertEqual(self.expected_line1, line2)

    def test_parser_status_ok_1(self):
        expected_status = 0
        status = DataParser('login dima').status
        self.assertEqual(status, expected_status)

    def test_parser_status_ok_2(self):
        expected_status = 0
        status = DataParser('msgall message').status
        self.assertEqual(status, expected_status)

    def test_parser_status_ok_3(self):
        expected_status = 0
        status = DataParser('msg dima hello').status
        self.assertEqual(status, expected_status)

    def test_parser_status_ok_4(self):
        expected_status = 0
        status = DataParser('userlist').status
        self.assertEqual(status, expected_status)

    def test_parser_status_ok_5(self):
        expected_status = 0
        status = DataParser('whoami').status
        self.assertEqual(status, expected_status)

    def test_parser_status_ok_6(self):
        expected_status = 0
        status = DataParser('logout').status
        self.assertEqual(status, expected_status)

    def test_parser_status_unknown_command(self):
        request = 'unknown command request'
        req_dict = DataParser(request)
        expected_status = -2
        self.assertEqual(req_dict.status, expected_status)

    def test_parser_status_require_username(self):
        request = 'login'
        req_dict = DataParser(request)
        expected_status = -10
        self.assertEqual(req_dict.status, expected_status)

    def test_parser_status_overage_info_logout(self):
        request = 'logout dima'
        req_dict = DataParser(request)
        expected_status = -11
        self.assertEqual(req_dict.status, expected_status)

    def test_parser_status_overage_info_msg(self):
        request = 'msg'
        req_dict = DataParser(request)
        expected_status = -11
        self.assertEqual(req_dict.status, expected_status)

    def test_parser_status_empty_message_all(self):
        request = 'msgall'
        req_dict = DataParser(request)
        expected_status = -20
        self.assertEqual(req_dict.status, expected_status)

    def test_parser_status_empty_message(self):
        request = 'msg dima'
        req_dict = DataParser(request)
        expected_status = -20
        self.assertEqual(req_dict.status, expected_status)

    def test_parser_args_logout(self):
        request = 'userlist'

        expected_cmd = 'userlist'
        expected_param = None
        expected_body = None

        cmd = DataParser(request).cmd
        param = DataParser(request).parameter
        body = DataParser(request).body

        self.assertEqual(cmd, expected_cmd)
        self.assertEqual(param, expected_param)
        self.assertEqual(body, expected_body)

    def test_parser_args_login(self):
        request = 'login dima'

        expected_cmd = 'login'
        expected_param = 'dima'
        expected_body = None

        cmd = DataParser(request).cmd
        param = DataParser(request).parameter
        body = DataParser(request).body

        self.assertEqual(cmd, expected_cmd)
        self.assertEqual(param, expected_param)
        self.assertEqual(body, expected_body)

    def test_parser_args_msg(self):
        request = 'msg Dima hello, dear friend!'

        expected_cmd = 'msg'
        expected_param = 'Dima'
        expected_body = ['hello,', 'dear', 'friend!']

        cmd = DataParser(request).cmd
        param = DataParser(request).parameter
        body = DataParser(request).body

        self.assertEqual(cmd, expected_cmd)
        self.assertEqual(param, expected_param)
        self.assertEqual(body, expected_body)


if __name__ == '__main__':
    unittest.main()
