from unittest import TestCase
import asyncio


class TestAsyncIO(TestCase):
    """
    Provides ``self.ioloop``, an ``asyncio`` event loop.
    """

    def __init__(self):
        super().__init__()
        self.ioloop = None

    def setUp(self):
        self.ioloop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.ioloop)
