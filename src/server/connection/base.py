from abc import ABCMeta, abstractmethod
from asyncio import Queue
import logging

from message import GameOver, Ping
from request import Login, Say, TakeExit, Pong
from exn import RPGException


class Connection(object):
    """Represents a connection to the RPG server"""

    __metaclass__ = ABCMeta

    class CannotReceive(RPGException):
        def __init__(self, exn):
            msg = f'Cannot receive: {exn}'
            super(Connection.CannotReceive, self).__init__(msg)

    class NotUnicode(RPGException):
        def __init__(self, line):
            msg = f'Not Unicode: {line}'
            super(Connection.NotUnicode, self).__init__(msg)

    class EOF(RPGException):
        def __init__(self):
            super(Connection.EOF, self).__init__('EOF')

    def __init__(self):
        self.queue = Queue()

    def __str__(self):
        return f"Connection to {self.server}"

    @property
    @abstractmethod
    def server(self):
        """Description of the server to which self is connected (a string)"""
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
    async def _recv_message(self):
        """
        Get the next CharMessage from the server.
        Used by self.handle_next_message. Not meant to be used by clients.

        Returns:
            CharMessage
        """
        raise NotImplementedError('Server.recv_message not implemented')

    @abstractmethod
    async def dequeue_next_non_ping_message(self):
        """
        Get the next CharMessage from the server that is not a Ping
        Returns:
            CharMessage
        """
        return await self.queue.get()

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
            msg = await self.dequeue_next_non_ping_message()
            if isinstance(msg, GameOver):
                raise msg
            elif isinstance(msg, cls):
                return msg

    async def handle_next_message(self):
        """
        Fills the queue with the next incoming (non-Ping) messages.
        To be run in a separate task, inside an infinite loop.
        """
        msg = await self._recv_message()
        logging.debug(f'Received {msg}')
        if isinstance(msg, Ping):
            logging.debug('About to pong')
            await self.send_request(Pong())
            logging.debug('Sent pong')
        else:
            logging.debug(f'About to enqueue {msg}')
            await self.queue.put(msg)
            logging.debug(f'Enqueued {msg}')

    async def enqueue_non_ping_messages(self):
        """To be run as a separate task"""
        logging.debug(f'Perpetually enqueuing non-ping messages')
        while True:
            await self.handle_next_message()

    #######################################################
    # requests

    async def take_exit(self, eid):
        await self.send_request(TakeExit(eid))

    async def say(self, speech):
        await self.send_request(Say(speech))
