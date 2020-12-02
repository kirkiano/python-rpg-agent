
import asyncio
import coloredlogs
import os

from bot import parse_botline
from connect import Connection
from scrape import scrapers
from scrape.bot import ScrapingBot
from args import parse_args


def get_bots(ioloop, server_address, botfile, bot_params):
    """
    Construct the scraping bots stipulated in a given botfile.
    See :module:`bot.parse` for format of botfiles.

    Args:
        ioloop (:obj:`ioloop`):
        server_address (:obj:`Connection.SocketAddress`):
        botfile (str): path to the botfile
        bot_params (:obj:`ScrapingBot.Params`):

    Returns:
        :obj:`list` of :obj:`ScrapingBot`
    """
    def make_bot(name, password, address):
        return ScrapingBot.create(name, password, server_address, ioloop,
                                  getattr(scrapers, 'scrape_' + name),
                                  address, bot_params)
    with open(botfile, 'r') as f:
        return map(make_bot, map(parse_botline, f.readlines()))


def main(server_address, botfile, bot_params):
    ioloop = asyncio.get_event_loop()
    bots = get_bots(ioloop, server_address, botfile, bot_params)
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
    SERVER_ADDRESS = Connection.SocketAddress(ARGS.host, ARGS.port)
    BOT_PARAMS = ScrapingBot.Params(ARGS.ntitles,
                                    ARGS.waitleave,
                                    ARGS.waitdl)
    main(SERVER_ADDRESS, ARGS.botfile, BOT_PARAMS)
