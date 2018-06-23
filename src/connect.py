import asyncio
import json

from message import ServerMessage, Welcome, Place


class Connection(object):

    @staticmethod
    async def login(host, port, user, pw, ioloop):
        conn = Connection(host, int(port), ioloop)
        await conn.open()
        await conn.authenticate(user, pw)
        return conn

    class CannotAuthenticate(Exception):
        def __init__(self):
            self.msg = 'Cannot authenticate with given credentials'

    def __init__(self, host, port, ioloop):
        self.host = host
        self.port = port
        self.ioloop = ioloop
        self.reader = None
        self.writer = None

    @asyncio.coroutine
    def open(self):
        self.reader, self.writer = yield from asyncio.open_connection(
            self.host, self.port, loop=self.ioloop)

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

    async def authenticate(self, user, pw):
        await self.send_message({
            'type': 'login',
            'creds': {'user': user, 'pass': pw}
        })
        resp = await self.recv_message()
        if not isinstance(resp, Welcome):
            raise Connection.CannotAuthenticate()

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
