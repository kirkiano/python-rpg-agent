from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://www.cato.org')
def scrape_catoinst(soup):
    tags = [dict(id=uuid4(), title=t.text) for t in soup.find_all('article')]
    return tags


SCRAPERS = [scrape_catoinst]
