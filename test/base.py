from unittest import TestCase
import asyncio


class TestAsyncIO(TestCase):

    def setUp(self):
        self.ioloop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.ioloop)
