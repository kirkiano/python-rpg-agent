from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


def scrape_freespeech():
    html = get_web_page('https://freespeech.org/')
    soup = BeautifulSoup(html, 'html.parser')

    return [dict(id=uuid4(), title=t.find('p').text)
            for t in soup.find_all('div', {'class': 'story-caption'})]


SCRAPERS = [scrape_freespeech]
