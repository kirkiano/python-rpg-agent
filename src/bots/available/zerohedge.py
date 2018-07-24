from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://www.zerohedge.com')
def scrape_zerohedge(soup):
    tags = soup.find_all('article')
    return [dict(id=uuid4(), title=t.text) for t in tags]


SCRAPERS = [scrape_zerohedge]
