from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://mises.org')
def scrape_mises(soup):
    tags = soup.find_all(class_='teaser-title')
    return [dict(id=uuid4(), title=t.contents[0].text) for t in tags]


SCRAPERS = [scrape_mises]
