"""
Scraper abstractions
"""

from functools import partial, wraps
import json

from bs4 import BeautifulSoup

from web import get_web_page


def scraper(url, parse):
    """
    Creates a decorator that downloads a web page, parses it, and returns
    those parts of it that are of interest.

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
            raw_content = await get_web_page(url)
            parsed_content = parse(raw_content)
            try:
                return extract(parsed_content)
            except Exception as e:
                print(f'Cannot extract from {url}:')
                raise e

        return go

    return decorator


json_scraper = partial(scraper, parse=json.loads)

html_scraper = partial(scraper,
                       parse=lambda html: BeautifulSoup(html, 'html.parser'))
