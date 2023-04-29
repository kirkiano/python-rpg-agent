from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from .roam_action import RoamingAction
from bot import Bot
from server import MockConnection
from model import Direction, Place as PlaceModel
from message import Place, Exit, WaysOut
from request import TakeExit


class TestRoam(IsolatedAsyncioTestCase):

    async def test_roam_unconfined(self):
        place_1 = PlaceModel(1, 'some place',       '', None)
        place_2 = PlaceModel(2, 'some other place', '', None)
        exits = [Exit(42, Direction.NORTH, '', place_2)]
        mock_null_action = AsyncMock()
        action = RoamingAction(1, mock_null_action)
        conn = MockConnection()

        # prep the connection
        await conn.enqueue_message(Place(place_1))
        await conn.enqueue_message(WaysOut(exits))
        bot = Bot(conn, 'dummy bot', action)
        await action(bot)
        req = await conn.dequeue_request()
        self.assertEqual(req, TakeExit(exits[0].id))
