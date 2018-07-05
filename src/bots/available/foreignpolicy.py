from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


def scrape_foreignpolicy():
    html = get_web_page('http://foreignpolicy.com')
    soup = BeautifulSoup(html, 'html.parser')
    return [dict(id=uuid4(), title=t.text.strip())
            for t in soup.find_all('a', {'class': 'hed-heading'})]


SCRAPERS = [scrape_foreignpolicy]
