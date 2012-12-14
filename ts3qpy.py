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
        """
        Connects to Teamspeak 3 server on host:port
        Checks the telnet output for teamspeak server
        """
        self.logger.debug('Connecting to %s:%s' % (self.host, self.port))
        self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
        self.logger.debug('Connected')
        self.logger.debug('Testing connection')
        reply = self.read('TS')

        # Check if it is TS3 server
        if reply != 'TS':
            self.logger.error('Server is not Teamspeak 3 server')
            raise ConnectionFailed

        self.read(timeout=0.1)  # clear buffer
        self.logger.debug('Connection established successfully, buffer is cleared')

    def disconnect(self):
        """
        Disconnects from the server if there is active connection
        """
        if self.tn:
            self.logger.debug('Connection closed')
            self.tn.close()
            self.tn = None

    def read(self, until='msg=ok', timeout=None):
        if not timeout:
            timeout = self.timeout
        self.logger.debug('Receiving message with timeout of %s seconds until "%s"' % (timeout, until))
        return self.tn.read_until(until, timeout)

    def write(self, msg):
        return self.tn.write(msg)

    def command(self, cmd, timeout=None):
        """
        Returns the telnet reply from server after executing command cmd
        :type cmd: str
        """
        if not timeout:
            timeout = self.timeout
        self.logger.debug('Executing command %s' % cmd)
        self.write(cmd + '\n')
        reply = self.read(timeout=timeout)
        self.logger.debug('Received %s chars' % len(reply))
        return reply

#if __name__ == '__main__':
#    q = QueryClient('cygame.ru')
#    q.connect()
#    s = q.command('help')
#    print s.split('\n')[-1]
