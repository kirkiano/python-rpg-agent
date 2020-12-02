import datetime
import asyncio
import random
from collections import defaultdict, namedtuple
import logging

from bot import Bot
from connect import Connection
from message import Place, WaysOut


class ScrapingBot(Bot):
    """A ``Bot`` that scrapes websites."""

    # see parse_args for meanings of these params
    Params = namedtuple('Params', 'ntitles, waitleave, waitdl')

    class NotHome(Exception):
        def __init__(self, address_exp, address_act):
            self.address_exp = address_exp
            self.address_act = address_act

        def __str__(self):
            return f'Expected to be at {self.address_exp},' \
                   f' not {self.address_act.name}.'

    @staticmethod
    def create(name, password, server, ioloop, scraper, address, bot_params):
        creds = Connection.Credentials(name, password)
        return ScrapingBot(server=server,
                           credentials=creds,
                           ioloop=ioloop,
                           download_func=scraper,
                           params=bot_params,
                           address_name=address)

    def __init__(self, server, credentials, ioloop, download_func, params,
                 address_name, do_shuffle=True):
        """
        Args:
            server (Connection.Server): server to log in to
            credentials (Connection.Credentials): credentials for login
            ioloop (asyncio.ioloop):
            download_func: async func that downloads and scrapes this bot's
                    target content, returning a list of dicts, each having
                    two keys: id & title
            params (ScrapingBot.Params):
            address_name (str): name of the address to which this scraping bot
                                should be confined
            do_shuffle (bool): randomize the order of headlines
        """
        super(ScrapingBot, self).__init__(server, credentials, ioloop)
        self.download_func = download_func
        self.params = params
        self.do_shuffle = do_shuffle
        self.headlines = []
        self.seen = defaultdict(set)
        self.place = None
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
        while True:
            await self._run_iteration()

    async def _run_iteration(self):
        self.place = (await self.conn.wait_for(Place)).place
        if not self.is_home(self.place.address):
            raise ScrapingBot.NotHome(self.home_address, self.place.address)
        self.exits = (await self.conn.wait_for(WaysOut)).exits
        logging.info(f'{self.conn.user} is now in {self.place}.')
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
            logging.info(f'{self.conn.user} has downloaded its content.')

    async def _speak_headlines(self):
        """
        Announce (at most) the next ntitles headlines.
        """
        unseen_headlines = [p for p in self.headlines
                            if p['id'] not in self.seen[self.place.id]]
        if self.do_shuffle:
            random.shuffle(unseen_headlines)
        num_headlines_to_speak = min(self.params.ntitles, len(unseen_headlines))
        for headline in unseen_headlines[:num_headlines_to_speak]:
            saying = headline['title'].strip()
            await self.conn.say(saying)
            logging.debug(f'{self.conn.user} has said: {saying}.')
            self.seen[self.place.id].add(headline['id'])
