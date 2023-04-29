import asyncio

from .base import Connection


class MockConnection(Connection):

    def __init__(self):
        super().__init__()
        self._reqs = []
        self._msgs = []
        self._reqs_lock = asyncio.Lock()
        self._msgs_lock = asyncio.Lock()

    @property
    def server(self):
        return "mock server"

    async def send_request(self, request):
        """
        See superclass docstring
        """
        async with self._reqs_lock:
            self._reqs.append(request)

    async def recv_message(self):
        """
        See superclass docstring
        """
        async with self._msgs_lock:
            return self._msgs.pop(0)

    async def dequeue_request(self):
        """
        Dequeue the next Request sent via this mock connection.
        """
        async with self._reqs_lock:
            return self._reqs.pop(0)

    async def enqueue_message(self, message):
        """
        Enqueue a Message to be received via this mock connection.
        """
        async with self._msgs_lock:
            return self._msgs.append(message)
