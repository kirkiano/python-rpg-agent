import asyncio
import json
import logging
from collections import namedtuple

from message import ServerMessage, Welcome
from request import (TakeExit, Say)


class Connection(object):
    """Object representing a connection to the RPG server."""

    SocketAddress = namedtuple('SocketAddress', 'host, port')
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
            server.host,
            server.port,
            loop=self.ioloop)
        self.server = server

    def close(self):
        self.reader = self.writer = None
        self.writer.close()

    async def authenticate(self, credentials):
        await self._send_dict({
            'type': 'login',
            'creds': {'user': credentials.user,
                      'pass': credentials.pw}
        })
        await self.wait_for(Welcome)
        self.credentials = credentials

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
    def take_exit(self, eid):
        yield from self._send_request(TakeExit(eid))

    @asyncio.coroutine
    def say(self, speech):
        yield from self._send_request(Say(speech))

    # @asyncio.coroutine
    # def who_am_i(self):
    #     yield from self._send_request(WhoAmI())

    # @asyncio.coroutine
    # def where_am_i(self):
    #    yield from self._send_request(WhereAmI())

    # @asyncio.coroutine
    # def what_is_here(self):
    #     yield from self._send_request(WhatIsHere())

    # @asyncio.coroutine
    # def how_can_i_exit(self):
    #    yield from self._send_request(HowCanIExit())

    # @asyncio.coroutine
    # def edit_me(self, desc):
    #     yield from self._send_request(EditMe(desc))
    #
    # @asyncio.coroutine
    # def describe_thing(self, tid):
    #     yield from self._send_request(DescribeThing(tid))

    # @asyncio.coroutine
    # def whisper(self, speech, tid):
    #     yield from self._send_request(Whisper(speech, tid))
    #
    #######################################################

    @asyncio.coroutine
    def _send_request(self, request):
        """
        Asynchronously send a request to the RPG server. This method
        is used by other methods and should not be used directly.

        Args:
            request (Request):
        """
        yield from self._send_dict(request.to_dict())

    @asyncio.coroutine
    def _send_dict(self, request):
        """
        Asynchronously send a dictionary to the RPG server. This method
        is used by other methods and should not be used directly.

        Args:
            request (dict):
        """
        request_json = json.dumps(request)
        logging.debug(f'Sending {request_json}')
        self.writer.write((request_json + '\r\n').encode('utf-8'))
        yield from self.writer.drain()
