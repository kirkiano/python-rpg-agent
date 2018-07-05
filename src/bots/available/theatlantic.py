from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


def scrape_theatlantic():
    html = get_web_page('http://freespeech.org/')
    soup = BeautifulSoup(html, 'html.parser')
    return [dict(id=uuid4(), title=t.text.strip())
            for t in soup.find_all('h2', {'class': 'o-hed'})]


SCRAPERS = [scrape_theatlantic]
