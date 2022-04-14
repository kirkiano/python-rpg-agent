from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from message import Place, WaysOut, Welcome
from model import Address, Direction, Exit, Place as PlaceModel
from request import Say, TakeExit
from server.connection.mock import MockConnection
from scrape.bot import ScrapingBot


def async_mock(*args, **kwargs):
    """See https://blog.miguelgrinberg.com/post/unit-testing-asyncio-code"""
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*co_args, **co_kwargs):
        return m(*co_args, **co_kwargs)

    mock_coro.mock = m
    return mock_coro


_MOCK_ADDRESS_NAME = 'some_game_address'
_MOCK_WELCOME = Welcome(1, 'some_char_name', 'some_char_desc', 1.0)
_MOCK_ADDRESS = Address(1, _MOCK_ADDRESS_NAME, 42,
                        'some_street',
                        'some_city',
                        'some_country')

_MOCK_PLACE_ID = 1
_MOCK_PLACE = PlaceModel(_MOCK_PLACE_ID, 'some_place', 'some_place_desc',
                         _MOCK_ADDRESS)

_MOCK_EXIT_ID = 42
_MOCK_EXIT = Exit(_MOCK_EXIT_ID, Direction.NORTH, 'some_portal', _MOCK_PLACE)

_MOCK_EXITS = {
    _MOCK_PLACE_ID: [_MOCK_EXIT]
}

_MOCK_HEADLINE = 'Sample headline'
_MOCK_HEADLINES = [{'id': 1, 'title': _MOCK_HEADLINE}]
_MOCK_SCRAPER = async_mock(return_value=_MOCK_HEADLINES)


class TestScrapingBot(IsolatedAsyncioTestCase):

    async def test_bot_run_iteration(self):
        ntitles = 1 + len(_MOCK_HEADLINES)
        waitleave = 0  # seconds
        waitdl = 0  # minutes
        bot_params = ScrapingBot.Params(ntitles, waitleave, waitdl)
        conn = MockConnection.create()
        await conn.messages.put(_MOCK_WELCOME)
        bot = await ScrapingBot.create(conn, _MOCK_SCRAPER, _MOCK_ADDRESS_NAME,
                                       bot_params)

        self.assertIsNone(bot.current_place)
        await conn.messages.put(Place(_MOCK_PLACE))
        await conn.messages.put(WaysOut(_MOCK_EXITS[_MOCK_PLACE.id]))

        await bot._run_iteration()

        self.assertIsNotNone(bot.current_place)
        self.assertIsNotNone(bot.current_place.address)
        self.assertEqual(bot.current_place.address.name, _MOCK_ADDRESS_NAME)

        request = await conn.requests.take()
        self.assertEqual(request, Say(_MOCK_HEADLINE))

        request = await conn.requests.take()
        self.assertEqual(request, TakeExit(_MOCK_EXIT_ID))
