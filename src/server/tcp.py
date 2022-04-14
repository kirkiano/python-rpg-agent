import asyncio
from collections import namedtuple

from exn import RPGException
from .base import Server
from .connection import TCPConnection


class TCPServer(Server):

    Address = namedtuple('ServerAddress', 'host, port')

    class CannotConnect(RPGException):
        def __init__(self, address, exn):
            msg = f'Cannot connect to server at {address}: {exn}'
            super(TCPServer.CannotConnect, self).__init__(msg)

    def __init__(self, address):
        self._address = address

    def __str__(self):
        return f'TCP server at {self.address}'

    @property
    def address(self):
        return self._address

    async def connect(self):
        """See superclass docstring"""
        try:
            reader, writer = await asyncio.open_connection(self.address.host,
                                                           self.address.port)
            return TCPConnection(self.address, reader, writer)
        except Exception as e:
            raise TCPServer.CannotConnect(self.address, e)
