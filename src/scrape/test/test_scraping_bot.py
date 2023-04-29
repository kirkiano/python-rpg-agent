# from unittest import IsolatedAsyncioTestCase
#
# from message import Place, WaysOut, Welcome
# from model import mock_exit
# from request import Say, TakeExit
# from server.connection.mock import MockConnection
# from scrape.scrapers.mock import MockScraper
#
#
# class TestScrapingBot(IsolatedAsyncioTestCase):
#
#     async def test_bot_run_iteration(self):
#         """
#         Test that one iteration of a scraping bot's loop will scrape headlines,
#         speak one of them, and then move to the next place.
#         """
#         welcome = Welcome(1, 'some_char_name', 'some_char_desc', 1.0)
#         egress = mock_exit()  # 'exit' is a Python built-in, hence 'egress'
#         scraper = MockScraper.create()
#         bot_params = ScrapingBot.Params(ntitles=len(scraper), waitleave=0, waitdl=0)
#         conn = MockConnection()
#         await conn.enqueue_message(welcome)
#         bot = await ScrapingBot.create(
#             conn, scraper,
#             game_address=egress.neighbor.address.name,
#             bot_params=bot_params)
#
#         self.assertIsNone(bot.current_place)
#         await conn.enqueue_message(Place(egress.neighbor))
#         await conn.enqueue_message(WaysOut([egress]))
#
#         await bot._run_iteration()
#
#         self.assertIsNotNone(bot.current_place)
#         self.assertEqual(bot.current_place.address, egress.neighbor.address)
#
#         headlines = scraper.headlines()
#         request = await conn.dequeue_request()
#         next_headline = next(headlines)['title']
#         self.assertEqual(request, Say(next_headline))
#
#         request = await conn.dequeue_request()
#         self.assertEqual(request, TakeExit(egress.id))
