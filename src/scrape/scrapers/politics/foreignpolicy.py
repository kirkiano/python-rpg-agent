from uuid import uuid4

from scrape.decorators import html_scraper


@html_scraper('https://foreignpolicy.com')
def scrape_foreignpolicy(soup):
    return [dict(id=uuid4(), title=t.text.strip())
            for t in soup.find_all('a', {'class': 'hed-heading'})]


SCRAPERS = [scrape_foreignpolicy]
