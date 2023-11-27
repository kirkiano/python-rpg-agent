import json
import logging

from message import CharMessage, Ping
from .auto_pong import Connection, AutoPongConnection


logger = logging.getLogger('tcp')
logger.propagate = False


class TCPConnection(AutoPongConnection):
    """Object representing a connection to the RPG server."""

    def __init__(self, address, reader, writer):
        super().__init__()
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
        bs = (j + '\r\n').encode('utf-8')
        logger.debug(f'{self.username} sending: {bs}')
        self.writer.write(bs)
        await self.writer.drain()

    async def recv_message(self):
        """See superclass docstring"""
        bs = await self.reader.readline()
        logger.debug(f'{self.username} received: {bs}')
        if not bs:  # empty byte string
            # Since the Python docs for readline
            # (https://docs.python.org/3/library/asyncio-stream.html#asyncio.StreamReader.readline)
            # are a little ambiguous, it may help to note that
            # https://stackoverflow.com/a/35210204 confirms that
            # empty bytes means EOF.
            raise Connection.EOF()
        try:
            line = bs.decode('utf-8')
        except UnicodeError:
            raise Connection.NotUnicode(bs)
        # The 'else', though strictly unnecessary, reassures
        # the reader that 'line' is still in scope.
        else:
            if line.strip() == 'null':
                return Ping()
            else:
                try:
                    d = json.loads(line)
                    return CharMessage.from_object(d)
                except json.JSONDecodeError as e:
                    raise CharMessage.CannotParse(line, e)
