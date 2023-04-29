# from unittest.mock import MagicMock


class MockScraper(object):
    @staticmethod
    def create():
        mock_headlines = [{'id': 1, 'title': 'Sample headline'}]
        return MockScraper(mock_headlines)

    def __init__(self, headlines):
        self._headlines = headlines

    def __len__(self):
        """
        Number of unique headlines
        """
        return len(self._headlines)

    async def __call__(self):
        # return async_mock(return_value=_MOCK_HEADLINES)
        return self._headlines

    def headlines(self):
        """
        Generator enumerating the headlines
        """
        for headline in self._headlines:
            yield headline


# def create_mock_scraper(headlines):
#     """
#
#     Args:
#         headlines:
#
#     Returns:
#
#     """
#     async_mock(return_value=headlines)
#
#
# def async_mock(*args, **kwargs):
#     """See https://blog.miguelgrinberg.com/post/unit-testing-asyncio-code"""
#     m = MagicMock(*args, **kwargs)
#
#     async def mock_coro(*co_args, **co_kwargs):
#         return m(*co_args, **co_kwargs)
#
#     mock_coro.mock = m
#     return mock_coro
