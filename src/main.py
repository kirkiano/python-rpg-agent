import argparse
import asyncio
import coloredlogs
import os

from bot.connect import Connection
from scrape import scrapers
from scrape.bot import ScrapingBot


def parse_args():
    botfile_help = (
        'Text file in which each line has the name of a desired bot,'
        ' its password, and the RPG address to which it'
        ' should be confined, all separated by a single space. Any'
        ' whitespace inside the address name should be limited to one'
        ' space between its words, and no quote marks should be used'
        ' to delimit it.'
    )
    parser = argparse.ArgumentParser(
        description='RPG bots that scrape online periodicals',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--host',
        metavar='HOST',
        default='localhost',
        help='Hostname of server (live driver)'
    )
    parser.add_argument(
        'port',
        metavar='PORT',
        type=int,
        help='Port on server (live driver)'
    )
    parser.add_argument(
        'botfile',
        metavar='BOTFILE',
        help=botfile_help
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
    return parser.parse_args()


def parse_botfile(botfile):
    # User knows that the file should contain no blank lines
    with open(botfile, 'r') as f:
        contents = f.readlines()

    def make_bot_data_tuple(line):
        parts = line.split()
        if len(parts) < 3:
            raise Exception(f'botfile malformed at "{line}"')
        return parts[0], (parts[1], ' '.join(parts[2:]))

    return dict([make_bot_data_tuple(line) for line in contents])


def get_bots(ioloop, server, botfile, bot_params):
    def make_bot(name, scraper, password, address):
        creds = Connection.Credentials(name, password)
        return ScrapingBot(server=server,
                           credentials=creds,
                           ioloop=ioloop,
                           download_func=scraper,
                           params=bot_params,
                           address_name=address)

    bot_data = parse_botfile(botfile)
    scrapers_selected = {bn: getattr(scrapers, 'scrape_' + bn)
                         for bn in bot_data}
    bots = [make_bot(name, scrapers_selected[name], *pw_and_address)
            for (name, pw_and_address) in bot_data.items()]
    return bots


def main(server, botfile, bot_params):
    ioloop = asyncio.get_event_loop()
    bots = get_bots(ioloop, server, botfile, bot_params)
    tasks = [ioloop.create_task(bot.connect_and_run_safely()) for bot in bots]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()


if __name__ == '__main__':
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    print(f'Log level is {log_level}')

    # To change the format of log messages, see
    # https://docs.python.org/3/howto/logging.html#changing-the-format-of-displayed-messages
    # and https://docs.python.org/3/library/logging.html#logrecord-attributes
    coloredlogs.install(level=log_level,
                        fmt='%(asctime)s,%(msecs)03d %(levelname)s %(message)s')
    ARGS = parse_args()
    SERVER = Connection.Server(ARGS.host, ARGS.port)
    BOT_PARAMS = ScrapingBot.Params(ARGS.ntitles,
                                    ARGS.waitleave,
                                    ARGS.waitdl)
    main(SERVER, ARGS.botfile, BOT_PARAMS)
