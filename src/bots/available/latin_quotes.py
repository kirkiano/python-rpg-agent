from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_latinquotes():
    html = await get_web_page('https://en.wikiquote.org/wiki/Latin_proverbs')
    soup = BeautifulSoup(html, 'html.parser')
    italicizeds = soup.find_all('i')
    quotes = [dict(id=uuid4(), title=i.text) for i in italicizeds
              if i.parent.name == 'li']
    return quotes


SCRAPERS = [scrape_latinquotes]
