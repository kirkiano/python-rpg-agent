import os
import argparse
import asyncio
from importlib import import_module
from functools import reduce

from bots.scraping import ScrapingBot
from connect import Connection


def parse_args():
    parser = argparse.ArgumentParser(description='RPG bot')
    parser.add_argument(
        '--host',
        metavar='HOST',
        default='localhost',
        help='server hostname'
    )
    parser.add_argument(
        'port',
        metavar='PORT',
        type=int,
        help='server port'
    )
    parser.add_argument(
        '--ntitles',
        metavar='NTITLES',
        type=int,
        default=1,
        help='Max number of titles a bot announces per visit to a room'
    )
    parser.add_argument(
        '--waitleave',
        metavar='WAITLEAVE',
        type=int,
        default=1200,
        help='Maximum time (seconds) bot waits before leaving a room'
    )
    parser.add_argument(
        '--waitdl',
        metavar='WAITDL',
        type=int,
        default=1200,
        help='Maxmum time (minutes) bot waits before redownloading'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='Print verbose output',
        dest='verbose',
    )
    return parser.parse_args()


def get_bots(bot_params, ioloop, verbose=False):
    enabled_filenames = [f[:-3] for f in os.listdir('bots/enabled')
                         if f.endswith('.py') and f != '__init__.py']
    enabled_bot_modules = [
        import_module(f'bots.enabled.{f}') for f in enabled_filenames
    ]
    scraper_lists = [getattr(m, 'SCRAPERS')
                     for m in enabled_bot_modules if hasattr(m, 'SCRAPERS')]
    scrapers = reduce(lambda acc, ss: acc + ss, scraper_lists)
    bot_names = [scraper.__name__[7:] for scraper in scrapers]
    bots = [ScrapingBot(name=bot_name,
                        ioloop=ioloop,
                        download_func=scrape,
                        params=bot_params,
                        verbose=verbose)
            for bot_name, scrape in zip(bot_names, scrapers)]
    return bots


def main(server, bot_params, verbose=False):
    ioloop = asyncio.get_event_loop()
    bots = get_bots(bot_params, ioloop, verbose=verbose)
    tasks = [ioloop.create_task(bot.connect_and_run_safely(server))
             for bot in bots]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()


if __name__ == '__main__':
    clargs = parse_args()
    SERVER = Connection.Server(clargs.host, clargs.port)
    BOT_PARAMS = ScrapingBot.Params(
        clargs.ntitles,
        clargs.waitleave,
        clargs.waitdl)
    main(SERVER, BOT_PARAMS, clargs.verbose)
