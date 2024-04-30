from abc import ABCMeta, abstractmethod

from message import GameOver
from request import Login
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
            super().__init__(msg)

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
            super().__init__(msg)

    class EOF(RPGException):
        """
        Connection closed
        """
        def __init__(self):
            super().__init__('EOF')

    @property
    @abstractmethod
    def username(self):
        raise NotImplementedError('Connection.username not implemented')

    @property
    @abstractmethod
    def server(self):
        """
        Description of the server to which self is connected (a string)
        """
        raise NotImplementedError('Connection.server not implemented')

    @abstractmethod
    async def send_request(self, request):
        """
        Args:
            request (CharRequest)
        Returns: None
        """
        raise NotImplementedError('Connection.send_request not implemented')

    @abstractmethod
    async def recv_message(self):
        """
        Get the next CharMessage from the server.

        Returns:
            CharMessage
        """
        # Used by self.handle_next_message. Not meant to be used by clients.
        raise NotImplementedError('Connection.recv_message not implemented')

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
        Keep receiving messages from the server, until one of a given type
        is received, in which case return it.

        If GameOver is received, then raise it as an Exception

        Args:
            cls (type): a subclass of CharMessage. This
                        is the type of message to return, if received.

        Returns:
            CharMessage
        """
        while True:
            msg = await self.recv_message()
            if isinstance(msg, GameOver):
                raise msg
            elif isinstance(msg, cls):
                return msg
