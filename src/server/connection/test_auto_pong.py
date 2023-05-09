import asyncio
import unittest
from unittest.mock import patch, Mock

from .auto_pong import AutoPongConnection, Connection


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
        """
        Verify that an EOF kills the enqueue task of
        an AutoPongConnection.
        """
        _, task = MockAutoPongConnection.create()
        self.assertFalse(task.done())
        await asyncio.sleep(1)
        self.assertTrue(task.done())

    @patch.object(MockAutoPongConnection,
                  'recv_message',
                  Mock(side_effect=Connection.EOF))
    async def test_eof_raised_through(self):
        """
        Verify that an EOF is transferred to the main task of
        an AutoPongConnection.
        """
        conn, _ = MockAutoPongConnection.create()
        with self.assertRaises(Connection.EOF):
            await conn.recv_non_ping_message()
