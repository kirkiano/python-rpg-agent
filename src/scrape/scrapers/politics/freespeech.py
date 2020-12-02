from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://freespeech.org')
def scrape_freespeech(soup):
    return [dict(id=uuid4(), title=t.find('p').text)
            for t in soup.find_all('div', {'class': 'story-caption'})]


SCRAPERS = [scrape_freespeech]
