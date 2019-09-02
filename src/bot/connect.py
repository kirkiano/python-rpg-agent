import asyncio
import json
from collections import namedtuple

from common.server_message import ServerMessage, Welcome, SendCredentials
from common.request import (
    WhoAmI, WhereAmI, WhatIsHere, WaysOut, TakeExit, Say, Whisper,
    DescribeThing, EditMe
)


class Connection(object):
    """Object representing a connection to the RPG server."""

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

    @property
    def user(self):
        return self.credentials.user if self.credentials else None

    @asyncio.coroutine
    def open(self, server):
        self.reader, self.writer = yield from asyncio.open_connection(
            server.host, server.port, loop=self.ioloop)
        self.server = server

    def close(self):
        self.reader = self.writer = None
        self.writer.close()

    async def authenticate(self, credentials):
        await self.wait_for(SendCredentials)
        await self._send_dict({
            'type': 'login',
            'creds': {'user': credentials.user,
                      'pass': credentials.pw}
        })
        resp = await self.recv_message()
        if not isinstance(resp, Welcome):
            raise Connection.CannotAuthenticate()
        self.credentials = credentials

    @asyncio.coroutine
    def _send_dict(self, dct):
        """
        Asynchronously send a dictionary to the RPG server. This method
        is used by other methods below and should not be used directly.

        Args:
            dct (dict):
        """
        request = json.dumps(dct) + '\n'
        self.writer.write(request.encode('utf-8'))
        yield from self.writer.drain()

    @asyncio.coroutine
    def _send_request(self, request):
        """
        Asynchronously send a request to the RPG server. This method
        is used by other methods below and should not be used directly.

        Args:
            request (Request):
        """
        yield from self._send_dict(request.to_dict())

    @asyncio.coroutine
    def recv_message(self):
        while True:
            try:
                line = yield from self.reader.readline()
                j = json.loads(line.decode('utf-8'))
                msg = ServerMessage.from_json(j)
                return msg
            except ServerMessage.CannotParse:
                raise

    @asyncio.coroutine
    async def wait_for(self, cls):
        """
        Args:
            cls (type): one of the subclasses of ServerMessage

        Returns: the next-received ServerMessage of that type
        """
        while True:
            msg = await self.recv_message()
            if isinstance(msg, cls):
                return msg

    #######################################################
    # requests

    @asyncio.coroutine
    def who_am_i(self):
        yield from self._send_request(WhoAmI())

    @asyncio.coroutine
    def where_am_i(self):
        yield from self._send_request(WhereAmI())

    @asyncio.coroutine
    def what_is_here(self):
        yield from self._send_request(WhatIsHere())

    @asyncio.coroutine
    def ways_out(self):
        yield from self._send_request(WaysOut())

    @asyncio.coroutine
    def edit_me(self, desc):
        yield from self._send_request(EditMe(desc))

    @asyncio.coroutine
    def describe_thing(self, tid):
        yield from self._send_request(DescribeThing(tid))

    @asyncio.coroutine
    def take_exit(self, eid):
        yield from self._send_request(TakeExit(eid))

    @asyncio.coroutine
    def say(self, speech):
        yield from self._send_request(Say(speech))

    @asyncio.coroutine
    def whisper(self, speech, tid):
        yield from self._send_request(Whisper(speech, tid))
