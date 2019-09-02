from uuid import uuid4

from scrape.decorators import html_scraper


@html_scraper('https://theatlantic.org')
def scrape_theatlantic(soup):
    return [dict(id=uuid4(), title=t.text.strip())
            for t in soup.find_all('h2', {'class': 'o-hed'})]


SCRAPERS = [scrape_theatlantic]
