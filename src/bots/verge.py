from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


def scrape_verge(debug=False):
    r = get_web_page('https://www.theverge.com/', debug=debug)
    soup = BeautifulSoup(r, 'html.parser')
    tags = soup.find_all('h2', {'class': 'c-entry-box--compact__title'})
    return [dict(id=uuid4(), title=t.contents[0].text) for t in tags
            if hasattr(t.contents[0], 'text')]
