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
        logging.debug(f'Sending: {request}')
        d = request.to_dict()
        j = json.dumps(d)
        self.writer.write((j + '\r\n').encode('utf-8'))
        await self.writer.drain()

    async def recv_message(self):
        """See superclass docstring"""
        bytes = await self.reader.readline()
        logging.debug(f'Received bytes: {bytes}')
        if not bytes:  # empty byte string
            raise Connection.EOF()
        try:
            line = bytes.decode('utf-8')
        except UnicodeError as e:
            raise Connection.CannotReceive(e)
        else:
            if line.strip() == 'null':
                return Ping
            else:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError as e:
                    raise Connection.CannotReceive(e)
                else:
                    return CharMessage.from_object(d)
