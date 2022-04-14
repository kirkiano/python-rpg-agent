from abc import ABCMeta, abstractmethod

from message import GameOver
from request import Login, Say, TakeExit


class Connection(object):
    """Represents a connection to the RPG server"""

    __metaclass__ = ABCMeta

    def __str__(self):
        return f"Connection to {self.server}"

    @property
    @abstractmethod
    def server(self):
        """Description of the server to which self is connected (a string)"""
        pass

    @abstractmethod
    async def send_request(self, request):
        """
        Args:
            request (CharRequest)
        Returns: None
        """
        pass

    @abstractmethod
    async def recv_message(self):
        """
        Get the next CharMessage from the server
        Returns:
            CharMessage
        """
        pass

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

    async def wait_for(self, cls):
        """
        Keep receiving messages from the Server, until one of a given type
        is received, in which case return it.

        If GameOver is received, then raise it as an Exception

        Args:
            cls (type): one of the subclasses of CharMessage. This is the
                        type of message to return, if received.

        Returns:
            CharMessage
        """
        while True:
            msg = await self.recv_message()
            if isinstance(msg, GameOver):
                raise msg
            if isinstance(msg, cls):
                return msg

    #######################################################
    # requests

    async def take_exit(self, eid):
        await self.send_request(TakeExit(eid))

    async def say(self, speech):
        await self.send_request(Say(speech))
