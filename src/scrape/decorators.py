"""
Scraper decorators. html_scraper and json_scraper are defined at bottom.
"""

import json
from functools import partial, wraps

from bs4 import BeautifulSoup

from .download import download_web_page


class CannotParseHTML(Exception):
    def __init__(self, exn):
        msg = f'Cannot parse HTML: {exn}'
        super(CannotParseHTML, self).__init__(msg)


class CannotExtract(Exception):
    def __init__(self, exn):
        msg = f'Parsed successfully but could not extract, because: {exn}'
        super(CannotExtract, self).__init__(msg)


def _scraper(url, parse):
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
            try:  # apparently try/except creates no new scope in Python
                parsed_content = parse(raw_content)
            except Exception as e:
                raise CannotParseHTML(e)
            else:
                try:
                    return extract(parsed_content)
                except Exception as e:  # for generality, catch all exceptions
                    raise CannotExtract(e)

        return go

    return decorator


json_scraper = partial(_scraper, parse=json.loads)

html_scraper = partial(_scraper,
                       parse=lambda html: BeautifulSoup(html, 'html.parser'))
