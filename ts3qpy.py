# coding=utf8
import getpass
import sys
import telnetlib
import time
import logging


# ERRORS

class QueryError(Exception):
    pass


class ConnectionFailed(QueryError):
    pass


class NotATeaspeak3Server(ConnectionFailed):
    pass


class SocketError(ConnectionFailed):
    pass


# MAIN CLASS

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
        self.timeout = 1
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
        try:
            self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
        except telnetlib.socket.error:
            self.logger.error('No telnet server at %s:%s or connection timeout' % (self.host,self.port))
            raise SocketError
        self.logger.debug('Connected')
        self.logger.debug('Testing connection')
        reply = self.read('TS')

        # Check if it is TS3 server
        if reply != 'TS':
            self.logger.error('No Teamspeak 3 server at %s:%s' % (self.host,self.port))
            raise NotATeaspeak3Server

        self.read('command.\n\r', 0.5)  # clear buffer
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
        self.logger.debug('Receiving message with timeout of %s seconds until %s' % (timeout, repr(until)))
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

    def use(self, sid):
        self.command('use %s' % sid)

    def clientList(self):
        return self.command('clientlist')

    def say(self, message):
        self.command('gm %s' % message)

    def userCount(self):
        """
        Get real user count
        """
        return len(self.users())

    def users(self):
        d = str(self.clientList()).split('|')
        d[-1] = d[-1][:-19]
        users = []
        for x in d:
            recieved = {}
            for a in x.split(' '):
                data = a.split('=')
                if len(data) == 2:
                    recieved.update({data[0]: data[1]})
            if 'client_nickname' in recieved:
                users.append(recieved)
        normal_users = []
        for user in users:
            if user['client_type'] == '0':
                normal_users.append(user['client_nickname'])
        return normal_users

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def __del__(self):
        self.disconnect()