
import asyncio
import coloredlogs
import os

from bot import botfile_to_dict
from connect import Connection
from scrape import scrapers
from scrape.bot import ScrapingBot
from args import parse_args


def get_bots(ioloop, server_address, botfile, bot_params):
    """
    Construct the scraping bots stipulated in a given botfile.
    See :func:`botfile_to_dict` for botfile format.

    Args:
        ioloop (:obj:`ioloop`):
        server_address (:obj:`Connection.SocketAddress`):
        botfile (str): path of botfile
        bot_params (:obj:`ScrapingBot.Params`):

    Returns:
        :obj:`list` of :obj:`ScrapingBot`
    """
    bot_data = botfile_to_dict(botfile)
    return [ScrapingBot.create(name, password, server_address, ioloop,
                               getattr(scrapers, 'scrape_' + name),
                               address, bot_params)
            for (name, (password, address)) in bot_data.items()]


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
