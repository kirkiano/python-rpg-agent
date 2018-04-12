from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


def scrape_sciencemag(debug=False):
    r = get_web_page('http://www.sciencemag.org/', debug=debug)
    soup = BeautifulSoup(r, 'html.parser')
    tags = soup.find_all(class_=lambda a: a and a.startswith('media__headline'))
    headlines = [dict(id=uuid4(), title=t.text) for t in tags]
    return headlines
