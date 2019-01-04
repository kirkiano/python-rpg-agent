from unittest.mock import patch, MagicMock
import asyncio

from connect import Connection
from bots.bot import Bot
from test.base import TestAsyncIO
from rpg_object import Direction, Exit, Location
from message import Place


def async_mock(*args, **kwargs):
    """See https://blog.miguelgrinberg.com/post/unit-testing-asyncio-code"""
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro


def async_test(f):
    """See https://stackoverflow.com/questions/23033939/how-to-test-python-3-4-asyncio-code"""
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper


# Used also by TestScrapingBot (test_scraping_bot.py)
class MockConnection(object):
    def __init__(self):
        self.recv_message_mock = MagicMock()
        self.look_mock = MagicMock()
        self.say_mock = MagicMock()
        self.take_exit_mock = MagicMock()

        exit = Exit(1, 'a brown door', Direction.NORTH, False, (2, 'kitchen'))
        location = Location(1, 'living room', 'spacious', [exit])
        self.wait_for_place_mock = MagicMock(return_value=Place(location))

    async def recv_message(self, *args, **kwargs):
        return self.recv_message_mock(*args, **kwargs)

    async def look(self, *args, **kwargs):
        return self.look_mock(*args, **kwargs)

    async def wait_for_place(self, *args, **kwargs):
        return self.wait_for_place_mock(*args, **kwargs)

    async def say(self, *args, **kwargs):
        return self.say_mock(*args, **kwargs)

    async def take_exit(self, *args, **kwargs):
        return self.take_exit_mock(*args, **kwargs)


class TestBot(TestAsyncIO):

    @patch.object(Connection, 'login',
                  new=async_mock(return_value=MockConnection()))
    def test_bot_connect(self):
        bot = Bot('dummy', self.ioloop)
        server = Connection.Server('dummy_host', 'dummy_port')
        assert not Connection.login.mock.called

        self.ioloop.run_until_complete(bot.connect(server))

        Connection.login.mock.assert_called_once()
        mock_conn = Connection.login.mock.return_value
        mock_conn.recv_message_mock.assert_called_once()
