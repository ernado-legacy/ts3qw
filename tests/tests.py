import unittest

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
    pass

if __name__ == '__main__':
    unittest.main()
