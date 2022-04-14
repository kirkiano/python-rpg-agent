from bot import parse_botline
from scrape.bot import ScrapingBot
from scrape import scrapers
from util import keep_trying


async def get_scraping_bots(server, botfile, bot_params):
    """
    Construct the scraping bots stipulated in a given botfile.
    See :module:`bot.parse` for format of botfiles.

    Args:
        server (:obj:`Server`):
        botfile (str): path to the botfile
        bot_params (:obj:`ScrapingBot.Params`):

    Returns:
        :obj:`list` of :obj:`ScrapingBot`
    """
    async def make_bot(username, password, game_address):
        conn = await keep_trying(server.connect, 2, f'connect to {server}')
        await conn.login(username, password)
        scraper = getattr(scrapers, 'scrape_' + username)
        return await ScrapingBot.create(conn, scraper,
                                        game_address, bot_params)
    with open(botfile, 'r') as f:
        bot_lines = f.readlines()
        bot_param_tuples = list(map(parse_botline, bot_lines))
        return [await make_bot(*bot_params) for bot_params in bot_param_tuples]
