from abc import ABCMeta, abstractmethod
from traceback import print_exc

from connect import Connection


class Bot(object):
    __metaclass__ = ABCMeta
    """Abstract class implementing a bot."""

    def __init__(self, name, ioloop, verbose=False):
        """
        Args:
            name (string): bot name
            ioloop (asyncio.ioloop):
            verbose (bool):
        """
        super(Bot, self).__init__()
        self.name = name
        self.ioloop = ioloop
        self.verbose = verbose
        self.conn = None
        self.location = None

    def is_connected(self):
        return bool(self.conn)

    async def connect(self, server):
        """
        Args:
            server (Connection.Server):
        """
        self.conn = await Connection.login(
            server=server,
            credentials=self.credentials,
            ioloop=self.ioloop)
        if self.verbose:
            print(f'{self.name} has connected to the RPG server.')
        await self.conn.recv_message()  # welcome
        await self.conn.look()  # TODO: consider deleting this look

    @abstractmethod
    async def run(self):
        """The bot's main action"""
        pass

    @property
    @abstractmethod
    def credentials(self):
        """Return instance of Connection.Credentials."""
        pass

    async def connect_and_run_safely(self, server):
        """
        Safety wrapper for run(). Ensures that a crashing bot does not also
        crash the whole program.
        """
        try:
            await self.connect(server)
            await self.run()
        except Exception:  # catching all Exceptions is NOT too broad here
            print()
            print(f'{self.name} crashed:')
            print_exc()
