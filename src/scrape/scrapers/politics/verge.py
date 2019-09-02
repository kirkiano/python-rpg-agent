from uuid import uuid4

from scrape.decorators import html_scraper


@html_scraper('https://www.theverge.com')
def scrape_verge(soup):
    tags = soup.find_all('h2', {'class': 'c-entry-box--compact__title'})
    return [dict(id=uuid4(), title=tag.contents[0].text) for tag in tags
            if hasattr(tag.contents[0], 'text')]


SCRAPERS = [scrape_verge]
