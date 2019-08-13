from unittest.mock import patch

from rpg_client_utils.connect import Connection
from rpg_client_utils.test.test_bot import async_mock, MockConnection
from kirkiano_test_utils.asyncio import TestAsyncIO
from bot import ScrapingBot


class TestScrapingBot(TestAsyncIO):

    @patch.object(Connection, 'login',
                  new=async_mock(return_value=MockConnection()))
    def test_bot_run_iteration(self):
        headlines = [{'id': 1, 'title': 'Sample headline'}]
        download_func = async_mock(return_value=headlines)

        # make ntitles greater than available titles, to ensure that the
        # implementation (ScrapingBot) can handle it
        ntitles = 1 + len(headlines)

        waitleave = 0  # seconds
        waitdl = 0  # minutes
        bot_params = ScrapingBot.Params(ntitles, waitleave, waitdl)
        server = Connection.Server('dummy_host', 0)
        creds = Connection.Credentials('dummy_user', 'dummy_password')
        bot = ScrapingBot(server, creds, self.ioloop, download_func,
                          bot_params)
        server = Connection.Server('dummy_host', 'dummy_port')
        self.ioloop.run_until_complete(bot.connect())

        mock_conn = Connection.login.mock.return_value
        assert not download_func.mock.called
        assert not mock_conn.wait_for_place_mock.called
        assert not mock_conn.say_mock.called
        assert not mock_conn.take_exit_mock.called
        assert not mock_conn.look_mock.called

        self.ioloop.run_until_complete(bot._run_iteration())
        mock_conn.wait_for_place_mock.assert_called_once()
        mock_conn.say_mock.assert_called_once()
        mock_conn.take_exit_mock.assert_called_once()
        mock_conn.look_mock.assert_called_once()
