from abc import ABCMeta, abstractmethod

from message import GameOver, Ping
from request import Login, Pong
from exn import RPGException


class Connection(object):
    """
    Abstract class representing a connection to the RPG server
    """

    __metaclass__ = ABCMeta

    class CannotReceive(RPGException):
        """
        Cannot receive the next message from the server
        """
        def __init__(self, exn):
            msg = f'Cannot receive: {exn}'
            super(Connection.CannotReceive, self).__init__(msg)

    class NotUnicode(RPGException):
        """
        Cannot decode the bytes that came from the server into Unicode
        """
        def __init__(self, bs):
            """
            Args:
                bs (bytes): the sequence of bytes that fails to be Unicode
            """
            msg = f'Not Unicode: {bs}'
            super(Connection.NotUnicode, self).__init__(msg)

    class EOF(RPGException):
        """
        Connection closed
        """
        def __init__(self):
            super(Connection.EOF, self).__init__('EOF')

    def __init__(self):
        self.username = None

    def __str__(self):
        maybe_user = f"{self.username}'s" if self.username else ""
        return f'{maybe_user}connection to {self.server}'

    @property
    @abstractmethod
    def server(self):
        """
        Description of the server to which self is connected (a string)
        """
        raise NotImplementedError('Server.server not implemented')

    @abstractmethod
    async def send_request(self, request):
        """
        Args:
            request (CharRequest)
        Returns: None
        """
        raise NotImplementedError('Server.send_request not implemented')

    @abstractmethod
    async def recv_message(self):
        """
        Get the next CharMessage from the server.

        Returns:
            CharMessage
        """
        # Used by self.handle_next_message. Not meant to be used by clients.
        raise NotImplementedError('Server.recv_message not implemented')

    async def recv_non_ping_message(self):
        """
        Convenience that filters out incoming Pings, by responding
        to them with Pongs.
        Returns:
            CharMessage
        """
        while True:
            msg = await self.recv_message()
            if isinstance(msg, Ping):
                await self.send_request(Pong())
            else:
                return msg

    async def login(self, username, password):
        """
        Args:
            username (str)
            password (str)
        Returns:
            None
        """
        login_request = Login(username, password)
        await self.send_request(login_request)
        self.username = username

    async def wait_for(self, cls):
        """
        Keep receiving messages from the Server, until one of a given type
        is received, in which case return it.

        If GameOver is received, then raise it as an Exception

        Args:
            cls (type): a subclass of CharMessage that is not Ping. This
                        is the type of message to return, if received.

        Returns:
            CharMessage
        """
        while True:
            msg = await self.recv_non_ping_message()
            if isinstance(msg, GameOver):
                raise msg
            elif isinstance(msg, cls):
                return msg
