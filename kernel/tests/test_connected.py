import unittest


class ConnectedTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expected_line1 = 1

    def test_1(self):
        line2 = 1
        self.assertEqual(self.expected_line1, line2)


if __name__ == '__main__':
    unittest.main()
