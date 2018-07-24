from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://wolfstreet.com')
def scrape_wolfstreet(soup):
    tags = soup.find_all('h1', {'class': 'entry-title'})
    return [dict(id=uuid4(), title=t.contents[1].text) for t in tags
            if hasattr(t.contents[1], 'text')]


SCRAPERS = [scrape_wolfstreet]
