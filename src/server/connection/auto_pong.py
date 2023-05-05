from abc import ABCMeta, abstractmethod
import asyncio
import unittest
from unittest.mock import patch, Mock

from message import Ping, GameOver
from request import Pong
from .base import Connection


class AutoPongConnection(Connection):
    """
    Abstract class that responds automatically to pings.
    To achieve this, method enqueue_non_ping_message should
    be run as a separate task. Client code, including subclasses,
    should *not* call recv_message, and should receive messages
    by calling recv_non_ping_message instead.

    The superclass's wait_for is appropriately overriden.
    """

    __metaclass__ = ABCMeta

    @staticmethod
    def create():
        conn = AutoPongConnection()
        task = asyncio.create_task(conn.enqueue_non_ping_messages())
        return conn, task

    def __init__(self):
        """
        This constructor is not meant to be called by any function
        except AutoPongConnection.create.
        """
        super().__init__()
        self._msgs = asyncio.Queue()

    async def enqueue_non_ping_messages(self):
        """
        Filters out incoming Pings, and responds to them with Pongs.
        """
        try:
            while True:
                msg = await self.recv_message()
                if isinstance(msg, Ping):
                    await self.send_request(Pong())
                else:
                    await self._msgs.put(msg)
        except Connection.EOF as e:
            # Enqueuing the exception allows the bot's main task to
            # pick it up and allows this task to conclude gracefully.
            await self._msgs.put(e)

    async def recv_non_ping_message(self):
        msg = await self._msgs.get()
        if isinstance(msg, Connection.EOF):
            raise msg
        else:
            return msg

    async def wait_for(self, cls):
        """
        Like the superclass's wait_for, except cls must not be Ping,
        as a Ping will never be returned.
        """
        while True:
            msg = await self.recv_non_ping_message()
            if isinstance(msg, GameOver):
                raise msg
            elif isinstance(msg, cls):
                return msg

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


###########################################################
# test

class MockAutoPongConnection(AutoPongConnection):

    @staticmethod
    def create():
        conn = MockAutoPongConnection()
        task = asyncio.create_task(conn.enqueue_non_ping_messages())
        return conn, task

    def __init__(self):
        """
        This constructor is not meant to be called by any function
        except MockAutoPongConnection.create.
        """
        super().__init__()
        self._mock_inp = asyncio.Queue()
        self._mock_out = asyncio.Queue()

    @property
    def server(self):
        return "mock auto-pong server"

    async def send_request(self, req):
        """
        See superclass docstring
        """
        await self._mock_out.put(req)

    async def recv_message(self):
        """
        See superclass docstring
        """
        return await self._mock_inp.get()

    async def dequeue_request(self):
        """
        Dequeue the next Request sent via this mock connection.
        """
        return await self._mock_out.get()

    async def enqueue_message(self, msg):
        """
        Enqueue a Message to be received via this mock connection.
        """
        await self._mock_inp.put(msg)


class TestAutoPongConnection(unittest.IsolatedAsyncioTestCase):

    @patch.object(MockAutoPongConnection,
                  'recv_message',
                  Mock(side_effect=Connection.EOF))
    async def test_expire_enqueue_on_eof(self):
        _, task = MockAutoPongConnection.create()
        self.assertFalse(task.done())
        await asyncio.sleep(1)
        self.assertTrue(task.done())

    @patch.object(MockAutoPongConnection,
                  'recv_message',
                  Mock(side_effect=Connection.EOF))
    async def test_eof_raised_through(self):
        conn, _ = MockAutoPongConnection.create()
        with self.assertRaises(Connection.EOF):
            await conn.recv_non_ping_message()
