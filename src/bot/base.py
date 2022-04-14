import logging
import random
from abc import ABCMeta, abstractmethod

from exn import RPGClientException
from server.connection import Connection  # noqa: F401


class Bot(object):
    """Abstract class implementing a bot."""
    __metaclass__ = ABCMeta

    class NoExit(RPGClientException):
        def __init__(self, client_name):
            msg = 'no exit is available from this place'
            super(Bot.NoExit, self).__init__(client_name, msg)

    def __init__(self, connection, name):
        """
        Args:
            connection (Connection)
            name (str)
        """
        super(Bot, self).__init__()
        self.conn = connection
        self._name = name
        self.exits = []
        self._place = None

    @property
    def name(self):
        return self._name

    @property
    def current_place(self):
        """
        Returns (Place): current place, or None if not yet Welcomed
        """
        return self._place

    @current_place.setter
    def current_place(self, place):
        self._place = place

    def is_connected(self):
        return bool(self.conn)

    @abstractmethod
    async def run(self):
        """The bot's main action"""
        pass

    async def run_safely(self):
        """
        Safety wrapper for run(). Ensures that a crashing bot does not also
        crash the whole program.
        """
        try:
            await self.run()
        except Exception as e:  # for safety, catch all exceptions
            logging.fatal(f'{self.name} crashed: {e}')

    async def take_random_exit(self, is_good_exit=lambda _: True):
        """
        Leave the current place by an exit chosen at random, as long as
        the exit satisfies is_good_exit.
        """
        valid_exit_ids = [e.id for e in self.exits if is_good_exit(e)]
        if valid_exit_ids:
            chosen_exit = random.choice(valid_exit_ids)
            await self.conn.take_exit(chosen_exit)
        else:
            raise Bot.NoExit(self.name)
