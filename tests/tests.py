import unittest
import ts3qpy

HOST = '127.0.0.1'
PORT = 10011
TOKEN = ''


try:
    from local import *
except ImportError:
    pass


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


class InitCase(unittest.TestCase):
    def test_init(self):
        self.q.connect()

    def setUp(self):
        self.q = ts3qpy.QueryClient(HOST, PORT)

    def tearDown(self):
        self.q.disconnect()

if __name__ == '__main__':
    unittest.main()
