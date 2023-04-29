import asyncio
from collections import namedtuple

from .base import Server
from .connection import TCPConnection


class TCPServer(Server):
    """
    Class representing a server that accepts TCP connections
    """

    Address = namedtuple('ServerAddress', 'host, port')

    def __init__(self, address):
        self._address = address

    def __str__(self):
        return f'game TCP server at {self.address}'

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
            raise Server.CannotConnect(self, e)
