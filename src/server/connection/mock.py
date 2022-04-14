import asyncio_channel

from server import Connection


class MockConnection(Connection):

    @staticmethod
    def create(channel_size=16):
        requests = asyncio_channel.create_channel(channel_size)
        messages = asyncio_channel.create_channel(channel_size)
        return MockConnection(requests, messages)

    def __init__(self, requests, messages):
        """
        Args:
            requests (channel)
            messages (channel)
        """
        self.requests = requests
        self.messages = messages

    @property
    def server(self):
        return "mock server"

    async def send_request(self, request):
        """See superclass docstring"""
        await self.requests.put(request)

    async def recv_message(self):
        """See superclass docstring"""
        return await self.messages.take()
