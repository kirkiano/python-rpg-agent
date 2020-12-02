from unittest.mock import MagicMock

from model import Place, Address, Exit, Direction


class MockConnection(object):
    def __init__(self):
        self.recv_message_mock = MagicMock()
        self.wait_for_mock = MagicMock()
        self.who_am_i_mock = MagicMock()
        self.where_am_i_mock = MagicMock()
        self.what_is_here_mock = MagicMock()
        self.ways_out_mock = MagicMock()
        self.edit_me_mock = MagicMock()
        self.describe_thing_mock = MagicMock()
        self.take_exit_mock = MagicMock()
        self.say_mock = MagicMock()
        self.whisper_mock = MagicMock()
        addresses = [
            Address(1, 'Acropolis', 1, 'Main Street', 'Athens', 'Greece'),
            Address(2, 'Acropolis', 2, 'Main Street', 'Athens', 'Greece'),
        ]
        places = [
            Place(1, 'Temple of Athena', 'spacious', addresses[0]),
            Place(2, 'Temple of Aphrodite', 'spacious', addresses[1]),
        ]
        def reduced_place(place): return place.id, place.name, place.address
        exits = [
            Exit(1, 'an open doorway', Direction.NORTH, True,
                 (reduced_place(places[0]))),
            Exit(2, 'an open doorway', Direction.SOUTH, True,
                 (reduced_place(places[1]))),
        ]
        # self.wait_for_place_mock =
        #   MagicMock(return_value=PlaceMessage(places[0]))

    async def recv_message(self, *args, **kwargs):
        return self.recv_message_mock(*args, **kwargs)

    async def wait_for(self, *args, **kwargs):
        return self.wait_for_mock(*args, **kwargs)

    async def who_am_i(self, *args, **kwargs):
        return self.who_am_i_mock(*args, **kwargs)

    async def where_am_i(self, *args, **kwargs):
        return self.where_am_i_mock(*args, **kwargs)

    async def what_is_here(self, *args, **kwargs):
        return self.what_is_here_mock(*args, **kwargs)

    async def ways_out(self, *args, **kwargs):
        return self.ways_out_mock(*args, **kwargs)

    async def edit_me(self, *args, **kwargs):
        return self.edit_me_mock(*args, **kwargs)

    async def describe_thing(self, *args, **kwargs):
        return self.describe_thing_mock(*args, **kwargs)

    async def take_exit(self, *args, **kwargs):
        return self.take_exit_mock(*args, **kwargs)

    async def say(self, *args, **kwargs):
        return self.say_mock(*args, **kwargs)

    async def whisper(self, *args, **kwargs):
        return self.whisper_mock(*args, **kwargs)


def async_mock(*args, **kwargs):
    """See https://blog.miguelgrinberg.com/post/unit-testing-asyncio-code"""
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro
