from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from .blab import BlabbingAction


class TestBlabbingAction(IsolatedAsyncioTestCase):

    async def test_call_blabbing_action(self):
        some_saying = 'some saying'

        async def get_sayings():
            return [{'title': some_saying}]

        blabbing = BlabbingAction(get_sayings)

        bot = AsyncMock()
        bot.say.assert_not_called()
        await blabbing(bot)
        bot.say.assert_awaited_once_with(some_saying)
