import argparse
import asyncio

from rpg_client_utils.connect import Connection
from kirkiano_scraping_utils import scrapers
from rpg_periodical_scraper.bot import ScrapingBot


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
        'botfile',
        metavar='BOTFILE',
        help=('text file in which each line has the name of a desired bot'
              ' and its password, separated by whitespace')
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


def parse_botfile(botfile):
    # User knows that the file should contain no blank lines
    with open(botfile, 'r') as f:
        contents = f.readlines()
    return dict([tuple(line.split()) for line in contents])


def get_bots(ioloop, server, botfile, bot_params, verbose=False):
    def make_bot(name, password, scraper):
        creds = Connection.Credentials(name, password)
        return ScrapingBot(server=server,
                           credentials=creds,
                           ioloop=ioloop,
                           download_func=scraper,
                           params=bot_params,
                           verbose=verbose)
    bot_passwords = parse_botfile(botfile)
    scrapers_selected = {bn: getattr(scrapers, 'scrape_' + bn)
                         for bn in bot_passwords}
    bots = [make_bot(name, pw, scrapers_selected[name])
            for (name, pw) in bot_passwords.items()]
    return bots


def main(server, botfile, bot_params, verbose=False):
    ioloop = asyncio.get_event_loop()
    bots = get_bots(ioloop, server, botfile, bot_params, verbose)
    tasks = [ioloop.create_task(bot.connect_and_run_safely()) for bot in bots]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()


if __name__ == '__main__':
    ARGS = parse_args()
    SERVER = Connection.Server(ARGS.host, ARGS.port)
    BOT_PARAMS = ScrapingBot.Params(ARGS.ntitles,
                                    ARGS.waitleave,
                                    ARGS.waitdl)
    main(SERVER, ARGS.botfile, BOT_PARAMS, ARGS.verbose)
