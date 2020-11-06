import random
from abc import ABCMeta, abstractmethod
import logging
import asyncio

from .connect import Connection


class Bot(object):
    """Abstract class implementing a bot."""
    __metaclass__ = ABCMeta

    class NoExit(Exception):
        pass

    def __init__(self, server, credentials, ioloop):
        """
        Args:
            server (Connection.Server): server that this bot should connect to
            credentials (Connection.Credentials): credentials to login to server
            ioloop (asyncio.ioloop):
        """
        super(Bot, self).__init__()
        self.server = server
        self.credentials = credentials
        self.ioloop = ioloop
        self.exits = []
        self.conn = None

    @property
    def name(self):
        return self.credentials.user

    def is_connected(self):
        return bool(self.conn)

    async def connect(self):
        self.conn = await Connection.login(server=self.server,
                                           credentials=self.credentials,
                                           ioloop=self.ioloop)
        logging.info(f'{self.name} has connected to the RPG server.')

    @abstractmethod
    async def run(self):
        """The bot's main action"""
        pass

    async def connect_and_run_safely(self):
        """
        Safety wrapper for run(). Ensures that a crashing bot does not also
        crash the whole program.
        """
        try:
            desc = f'connect to game at {self.server}'
            await keep_trying(self.connect, 2, desc)
            await self.run()
        except Exception as e:
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
            raise Bot.NoExit()


async def keep_trying(f, wait_secs, desc):
    """
    Keep trying to invoke f until it succeeds, ie, until it doesn't throw an
    exception.

    Args:
        f (thunk): the computation to keep attempting
        wait_secs (int): number of seconds to wait before retrying
        desc (str): grammatical predicate describing f (eg, "connect to db")

    Returns:
        whatever f returns
    """
    n = 1
    while True:
        try:
            return await f()
        except Exception as e:
            logging.warning(f'Attempt no. {n} to {desc} has FAILED: {e}.'
                            f' Retrying in {wait_secs} seconds...')
            n += 1
            await asyncio.sleep(wait_secs)
