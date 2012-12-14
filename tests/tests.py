import unittest
import ts3qpy
import datetime

HOST = '127.0.0.1'
PORT = 10011
TOKEN = ''


try:
    from local import *
except ImportError:
    pass


class InitCase(unittest.TestCase):
    def setUp(self):
        self.q = ts3qpy.QueryClient(HOST, PORT)
        self.q.connect()
        self.start = datetime.datetime.now()

    def tearDown(self):
        self.q.disconnect()


class ConnectionCase(InitCase):
    def test_connect(self):
        self.assertNotEqual(self.q, None)


class TestCommands(InitCase):
    def test_command(self):
        reply = self.q.command('help')
        self.assertTrue(reply.endswith('ok'))

if __name__ == '__main__':
    unittest.main()
