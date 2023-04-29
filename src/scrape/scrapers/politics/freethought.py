from uuid import uuid4

from scrape import html_scraper
from scrape.util import find_all


@html_scraper('https://thefreethoughtproject.com')
def scrape_freethought(soup):
    return [dict(id=uuid4(), title=t.text)
            for t in find_all(soup, class_='l-grid--item')]


SCRAPERS = [scrape_freethought]
