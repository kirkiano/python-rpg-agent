from abc import ABCMeta, abstractmethod
from collections import namedtuple


class Server(object):
    __metaclass__ = ABCMeta

    Credentials = namedtuple('Credentials', ['username', 'password'])

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    async def connect(self):
        """
        Returns:
            Connection
        """
        pass

    async def connect_and_login(self, username, password):
        """
        Args:
            username (str)
            password (str)
        Returns:
            Connection
        """
        conn = await self.connect()
        await conn.login(username, password)
        return conn
