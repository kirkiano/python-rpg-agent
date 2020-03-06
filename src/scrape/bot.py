import datetime
import asyncio
import random
from collections import defaultdict, namedtuple

from bot.base import Bot
from common.server_message import Place, WaysOut


class ScrapingBot(Bot):
    """A ``Bot`` that scrapes websites."""

    # see parse_args for meanings of these params
    Params = namedtuple('Params', 'ntitles, waitleave, waitdl')

    def __init__(self, server, credentials, ioloop, download_func, params,
                 address_name, do_shuffle=True, verbose=False):
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
            verbose (bool):
        """
        super(ScrapingBot, self).__init__(server, credentials, ioloop,
                                          verbose=verbose)
        self.download_func = download_func
        self.params = params
        self.do_shuffle = do_shuffle
        self.headlines = []
        self.seen = defaultdict(set)
        self.place = None
        self.exits = []
        self.is_good_exit = lambda e: (
            e.nbr.address and e.nbr.address.name.lower() == address_name.lower()
        )
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
        await self.conn.where_am_i()
        self.place = (await self.conn.wait_for(Place)).place
        await self.conn.how_can_i_exit()
        self.exits = (await self.conn.wait_for(WaysOut)).exits
        if self.verbose:
            print(f'{self.conn.user} is now in {self.place}.')
        await self._maybe_scrape()
        await asyncio.sleep(3)  # wait a couple of seconds before speaking
        await self._speak_headlines()
        wait_to_move = random.uniform(0, self.params.waitleave)
        await asyncio.sleep(wait_to_move)
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
            if self.verbose:
                print(f'{self.conn.user} has downloaded its content.')

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
            if self.verbose:
                print(f'{self.conn.user} has said: {saying}.')
            self.seen[self.place.id].add(headline['id'])
