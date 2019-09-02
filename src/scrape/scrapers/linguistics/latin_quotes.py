from uuid import uuid4

from scrape.decorators import html_scraper


@html_scraper('https://en.wikiquote.org/wiki/Latin_proverbs')
def scrape_latinquotes(soup):
    italicizeds = soup.find_all('i')
    quotes = [dict(id=uuid4(), title=i.text) for i in italicizeds
              if i.parent.name == 'li']
    return quotes


SCRAPERS = [scrape_latinquotes]
