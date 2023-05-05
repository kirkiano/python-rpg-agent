import unittest
import asyncio

from exn import RPGException
from bot import Bot
from scrape import scrapers
from action import RoamingAction, ConfineToAddress, BlabbingAction


async def get_scraping_bot_tasks(connect, botfile, waitleave):
    """
    Construct the scraping bots stipulated in a given botfile.
    See :module:`bot.parse` for format of botfiles.

    Args:
        connect (func): async function that takes a username and returns
                        an AutoPongConnection to the server
        botfile (str): path to the botfile
        waitleave (int): number of seconds to wait before moving

    Returns:
        :obj:`list` of pairs of :obj:`ScrapingBot`s' and their
        respective connections
    """
    async def make_bot(username, password, game_address):
        conn = await connect(username)
        pong_task = asyncio.create_task(conn.enqueue_non_ping_messages())
        await conn.login(username, password)
        scraper = getattr(scrapers, 'scrape_' + username)
        blab_headlines = BlabbingAction(scraper)
        confine = ConfineToAddress(game_address)
        roam = RoamingAction(waitleave, blab_headlines, confine)
        bot = await Bot.create(conn, roam)
        return bot, pong_task

    with open(botfile, 'r') as f:
        bot_lines = f.readlines()
        bot_param_tuples = list(map(parse_botline, bot_lines))
        return [await make_bot(*bot_params) for bot_params in bot_param_tuples]


class MalformedBotfile(RPGException):
    def __init__(self, line):
        msg = f'botfile malformed at "{line}"'
        super(RPGException, self).__init__(msg)


def parse_botline(line):
    """
    Parse a bot line. It should contain three whitespace-separated fields:

      1. the bot's username in the RPG
      2. the password for that username
      3. the name of the address to which the bot should be confined

    It is not an error for the address name to contain internal whitespace,
    though each occurrence of that whitespace will be converted to a single
    space.

    Args:
        line (str):

    Returns:
        tuple: (bot name, password, address name)
    """
    parts = line.split()
    if len(parts) < 3:
        raise MalformedBotfile(line)
    return parts[0], parts[1], ' '.join(parts[2:])


###########################################################

class TestBotfile(unittest.TestCase):
    def test_rejects_only_name(self):
        with self.assertRaises(MalformedBotfile):
            parse_botline('just_a_name')

    def test_rejects_if_missing_address(self):
        with self.assertRaises(MalformedBotfile):
            parse_botline('just_a_name and_a_password')

    def test_accepts_proper_line(self):
        name = 'just_a_name'
        pw = 'and_a_password'
        addr = 'and           an     address'
        self.assertEqual((name, pw, 'and an address'),
                         parse_botline(f'{name}     {pw}  {addr}'))
