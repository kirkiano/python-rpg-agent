import asyncio
import datetime
import logging
import random
from collections import defaultdict, namedtuple

from bot import Bot
from server.connection import Connection  # noqa: F401
from exn import RPGClientException
from message import GameOver, Place, WaysOut, Welcome


class ScrapingBot(Bot):
    """A ``Bot`` that scrapes websites."""

    # see parse_args for meanings of these params
    Params = namedtuple('Params', 'ntitles, waitleave, waitdl')

    class NotHome(RPGClientException):
        def __init__(self, name, address_exp, address_act):
            msg = f'Expected to be at {address_exp}, not {address_act.name}.'
            super(ScrapingBot.NotHome, self).__init__(name, msg)

    @staticmethod
    async def create(connection, scraper, game_address, bot_params):
        """
        Construct a scraping bot
        Args:
            connection (Connection): to the server
            scraper: scraping function
            game_address (str): the RPG address through which the bot may roam
            bot_params (ScrapingBot.Params)

        Returns:
            ScrapingBot
        """
        welcome = await connection.wait_for(Welcome)
        return ScrapingBot(connection=connection,
                           name=welcome.name,
                           download_func=scraper,
                           params=bot_params,
                           address_name=game_address)

    def __init__(self, connection, name, download_func, params,
                 address_name, do_shuffle=True):
        """
        Args:
            connection (Connection): connection to server
            name (str): name of this bot
            download_func: async func that downloads and scrapes this bot's
                    target content, returning a list of dicts, each having
                    two keys: id & title
            params (ScrapingBot.Params):
            address_name (str): name of the RPG address to which this scraping
                                bot should be confined
            do_shuffle (bool): randomize the order of headlines
        """
        super(ScrapingBot, self).__init__(connection, name)
        self.download_func = download_func
        self.params = params
        self.do_shuffle = do_shuffle
        self.headlines = []
        self.seen = defaultdict(set)
        self.exits = []
        self.home_address = address_name
        self.is_home = lambda a: a and a.name.lower() == address_name.lower()
        self.is_good_exit = lambda e: self.is_home(e.nbr.address)
        # set time of last download far enough in the
        # past to trigger a fresh download
        long_interval = datetime.timedelta(minutes=1 + params.waitdl)
        self.t_last_download = datetime.datetime.now() - long_interval

    async def run(self):
        """
        Connect to the game, download target content specific to this bot, and
        walk around from room to room, announcing headlines from the content.
        """
        try:
            while True:
                await self._run_iteration()
        except GameOver as e:
            logging.info(f'{self.name} detected game-over: {e}')

    async def _run_iteration(self):
        self.current_place = (await self.conn.wait_for(Place)).place
        logging.info(f'{self.name} is now in {self.current_place}')
        self.exits = (await self.conn.wait_for(WaysOut)).exits
        if not self.is_home(self.current_place.address):
            raise ScrapingBot.NotHome(self.name,
                                      self.home_address,
                                      self.current_place.address)
        await self._maybe_scrape()
        await self._speak_headlines()
        waiting_period = random.uniform(0, self.params.waitleave)
        await asyncio.sleep(waiting_period)
        await self.take_random_exit(self.is_good_exit)

    async def _maybe_scrape(self):
        """
        Download and scrape the target content if enough time has passed since
        the last time it was scraped.
        """
        t_now = datetime.datetime.now()
        wait_to_download = random.uniform(0, self.params.waitdl)
        waiting_time = datetime.timedelta(minutes=wait_to_download)
        diff = t_now - self.t_last_download
        if diff > waiting_time:
            self.headlines = await self.download_func()
            self.t_last_download = t_now
            logging.info(f'{self.name} has downloaded its content.')

    async def _speak_headlines(self):
        """
        Announce (at most) the next ntitles headlines.
        """
        unseen_headlines = [
            p for p in self.headlines
            if p['id'] not in self.seen[self.current_place.id]
        ]
        if self.do_shuffle:
            random.shuffle(unseen_headlines)
        num_headlines_to_speak = min(self.params.ntitles,
                                     len(unseen_headlines))
        for headline in unseen_headlines[:num_headlines_to_speak]:
            saying = headline['title'].strip()
            await self.conn.say(saying)
            logging.debug(f'{self.name} has said: {saying}.')
            self.seen[self.current_place.id].add(headline['id'])
