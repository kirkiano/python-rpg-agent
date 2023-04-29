from uuid import uuid4

from scrape import html_scraper
from scrape.util import find_all


@html_scraper('https://aapt.scitation.org/journal/ajp')
def scrape_ajp(soup):
    tags = [dict(id=uuid4(), title=t.text)
            for t in find_all(soup, class_='title')]
    return tags


SCRAPERS = [scrape_ajp]
