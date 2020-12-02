from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://www.oathkeepers.org')
def scrape_oathkeep(soup):
    tags = soup.find_all(class_='su-post-title')
    sayings = [dict(id=uuid4(), title=t.contents[0].text) for t in tags]
    return sayings


SCRAPERS = [scrape_oathkeep]
