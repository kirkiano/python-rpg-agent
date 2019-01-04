import asyncio
import json
from collections import namedtuple

from message import ServerMessage, Welcome, Place


class Connection(object):

    Server = namedtuple('Server', 'host, port')

    Credentials = namedtuple('Credentials', 'user, pw')

    @staticmethod
    async def login(server, credentials, ioloop):
        conn = Connection(ioloop)
        await conn.open(server)
        await conn.authenticate(credentials)
        return conn

    class CannotAuthenticate(Exception):
        def __init__(self):
            self.msg = 'Cannot authenticate with given credentials'

    def __init__(self, ioloop):
        """
        Args:
            ioloop (asyncio ioloop):
        """
        self.ioloop = ioloop
        self.server = None
        self.reader = None
        self.writer = None
        self.credentials = None

    @asyncio.coroutine
    def open(self, server):
        self.reader, self.writer = yield from asyncio.open_connection(
            server.host, server.port, loop=self.ioloop)
        self.server = server

    @asyncio.coroutine
    def send_message(self, m):
        msg = json.dumps(m) + '\n'
        self.writer.write(msg.encode('utf-8'))
        yield from self.writer.drain()

    @asyncio.coroutine
    def recv_message(self):
        while True:
            try:
                line = yield from self.reader.readline()
                j = json.loads(line.decode('utf-8'))
                msg = ServerMessage.from_json(j)
                return msg
            except ServerMessage.CannotParse:
                continue  # skip uninteresting messages

    def close(self):
        self.reader = self.writer = None
        self.writer.close()

    async def authenticate(self, credentials):
        await self.send_message({
            'type': 'login',
            'creds': {'user': credentials.user,
                      'pass': credentials.pw}
        })
        resp = await self.recv_message()
        if not isinstance(resp, Welcome):
            raise Connection.CannotAuthenticate()
        self.credentials = credentials

    @asyncio.coroutine
    def look(self):
        yield from self.send_message({'type': 'whereami'})

    @asyncio.coroutine
    def take_exit(self, eid):
        yield from self.send_message({'type': 'exit', 'eid':  eid})

    @asyncio.coroutine
    def say(self, s):
        yield from self.send_message({'type': 'say', 'value': s})

    @asyncio.coroutine
    async def wait_for_place(self):
        while True:
            msg = await self.recv_message()
            if isinstance(msg, Place):
                return msg
