# coding=utf8
import getpass
import sys
import telnetlib
import time
import logging


class ConnectionFailed(Exception):
    pass


class QueryClient:
    """
    Teamspeak 3 Query client
    """

    def __init__(self, host, port=10011):
        """
        :type host: str
        :type port: int
        """
        self.host = host
        self.port = port
        self.timeout = 5
        self.tn = None
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s.%(msecs)d [%(levelname)s] %(message)s', r'%d.%m.%y %H:%M:%S')
        ch.setFormatter(formatter)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

    def connect(self):
        self.logger.debug('Connecting to %s:%s' % (self.host, self.port))
        self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
        self.logger.debug('Receiving message')
        reply = self.tn.read_until('TS', self.timeout)
        if reply != 'TS':
            self.logger.error('Server is not Teamspeak 3 server')
            raise ConnectionFailed
        self.logger.debug('Connected')

    def disconnect(self):
        if self.tn:
            self.logger.debug('Connection closed')
            self.tn.close()
            self.tn = None


HOST = "cygame.ru"
PORT = 10011
TIMEOUT = 5
#user = raw_input("Enter your remote account: ")
#password = getpass.getpass()

#tn = telnetlib.Telnet(HOST, port=10011, timeout=TIMEOUT)
#o = tn.read_until('TS3', TIMEOUT)
#print o
#tn.write('help\n')
#print tn.read_until('msg=ok', TIMEOUT)
if __name__ == '__main__':
    q = QueryClient('cygame.ru')
#
#if password:
#    tn.read_until("Password: ")
#    tn.write(password + "\n")
#
#tn.write("ls\n")
#tn.write("exit\n")
