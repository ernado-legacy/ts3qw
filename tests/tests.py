import unittest
import ts3qpy
import datetime

HOST = '127.0.0.1'
HOST_G = HOST
PORT = 10011
TOKEN = ''

from local import *


class ServerDeterminationTest(unittest.TestCase):
    def setUp(self):
        self.q = ts3qpy.QueryClient(HOST_G, 22)

    def test_connect_notTS3(self):
        error = False
        try:
            self.q.connect()
        except ts3qpy.ConnectionFailed:
            error = True
        self.assertTrue(error)

    def test_connect_socketError(self):
        error = False
        try:
            self.q.connect()
        except ts3qpy.ConnectionFailed:
            error = True
        self.assertTrue(error)

    def tearDown(self):
        self.q.disconnect()


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
    def test_command_help(self):
        reply = self.q.command('help')
        self.assertTrue(reply.endswith('ok'))


class TestWithStatement(unittest.TestCase):
    def test_with(self):
        with ts3qpy.QueryClient(HOST, PORT) as q:
            reply = q.command('help')
            self.assertTrue(reply.endswith('ok'))


#if __name__ == '__main__':
#    unittest.main()
