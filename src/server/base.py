from abc import ABCMeta, abstractmethod
from collections import namedtuple

from exn import RPGException


class Server(object):
    """
    An abstract class holding information about the game server,
    and presenting methods for connecting to it (ie, an abstract
    connection factory).
    """
    __metaclass__ = ABCMeta

    Credentials = namedtuple('Credentials', ['username', 'password'])

    class CannotConnect(RPGException):
        def __init__(self, server, exn):
            msg = f'Cannot connect to {server}: {exn}'
            super().__init__(msg)

    @abstractmethod
    def __str__(self):
        raise NotImplementedError('Server.__str__ not implemented')

    @abstractmethod
    async def connect(self):
        """
        Connect to this server.
        Returns:
            Connection
        Raises:

        """
        raise NotImplementedError('Server.connect not implemented')

    async def connect_and_login(self, username, password):
        """
        Convenience method for connecting to this server and
        logging into it.

        Args:
            username (str)
            password (str)
        Returns:
            Connection
        """
        conn = await self.connect()
        await conn.login(username, password)
        return conn
