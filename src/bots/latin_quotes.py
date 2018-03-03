from random import shuffle
from uuid import uuid4

from bs4 import BeautifulSoup

from util.web import get_web_page


def download_latin_quotes(debug=False):
    r = get_web_page('https://en.wikiquote.org/wiki/Latin_proverbs',
                     debug=debug)
    soup = BeautifulSoup(r, 'html.parser')
    italicizeds = soup.find_all('i')
    quotes = [dict(id=uuid4(), title=i.text) for i in italicizeds
              if i.parent.name == 'li']
    shuffle(quotes)
    return quotes
