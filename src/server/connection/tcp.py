import json

from message import CharMessage, Ping
from server.connection.base import Connection

import logging


class TCPConnection(Connection):
    """Object representing a connection to the RPG server."""

    def __init__(self, address, reader, writer):
        super(TCPConnection, self).__init__()
        self._address = address
        self.reader = reader
        self.writer = writer

    @property
    def address(self):
        """TCPServer.Address to which this is connected"""
        return self._address

    @property
    def server(self):
        """See superclass docstring"""
        return f'TCP server at {self.address}'

    async def send_request(self, request):
        """See superclass docstring"""
        d = request.to_dict()
        j = json.dumps(d)
        self.writer.write((j + '\r\n').encode('utf-8'))
        await self.writer.drain()

    async def recv_message(self):
        """See superclass docstring"""
        line = await self.reader.readline()
        line = line.decode('utf-8')
        if line.strip() == 'null':
            return Ping
        else:
            d = json.loads(line)
            return CharMessage.from_object(d)
