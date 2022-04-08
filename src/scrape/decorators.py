"""
Scraper decorators. html_scraper and json_scraper are defined at bottom.
"""

import json
import logging
from functools import partial, wraps

from bs4 import BeautifulSoup

from .download import download_web_page


def scraper(url, parse):
    """
    Function that produces a decorator which downloads a web page, parses it,
    and passes the parsed content to the decorated function, whose result it
    returns.

    Args:
        url (str): URL of the web page
        parse (func): parse the HTTP response body's raw content

    Returns:
        func: the decorator

    """
    def decorator(extract):
        """
        The decorator itself.

        Args:
            extract (func): extract desired data from the parsed content

        Returns:
            async func: downloads, parses, returns what extract returns,
                        and raises whatever exceptions extract might raise
        """

        @wraps(extract)
        async def go():
            raw_content = await download_web_page(url)
            parsed_content = parse(raw_content)
            try:
                return extract(parsed_content)
            except Exception as e:
                logging.error(f'Cannot extract from {url}:')
                raise e

        return go

    return decorator


json_scraper = partial(scraper, parse=json.loads)

html_scraper = partial(scraper,
                       parse=lambda html: BeautifulSoup(html, 'html.parser'))
