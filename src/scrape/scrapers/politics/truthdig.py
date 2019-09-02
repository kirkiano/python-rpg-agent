from uuid import uuid4

from scrape.decorators import html_scraper


@html_scraper('https://www.truthdig.com')
def scrape_truthdig(soup):
    attr = 'archive-home__title'
    tags = soup.find_all(class_=lambda a: a and a.startswith(attr))
    sayings = [tag.contents[1].text for tag in tags]
    return [dict(id=uuid4(), title=s) for s in sayings]


SCRAPERS = [scrape_truthdig]
